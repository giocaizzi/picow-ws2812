/*
 * Ledwall Enclosure - Prototype v1
 *
 * Parametric enclosure for 40x32 WS2812B LED wall
 * with Raspberry Pi Pico W controller.
 *
 * Setup:
 *   5x 8x32 flexible LED matrix panels (10mm pitch)
 *   stacked vertically → 40 rows × 32 cols
 *   Elevated shelf with wiring channels (Schema 2 power injection)
 *   Raspberry Pi Pico W controller (bottom rear)
 *   DC barrel jack 5.5×2.1mm power input
 *   Wall-mounted via blind nail hole (top center)
 *
 * Coordinate system:
 *   X = width  (horizontal, left → right)
 *   Y = height (vertical,   bottom → top)
 *   Z = depth  (back → front)
 *
 * Two printable parts:
 *   1. Enclosure body (back panel + walls + internal features)
 *   2. Diffuser cover  (translucent front panel, press-fit)
 */

// ================================================================
// PARAMETERS
// ================================================================

/* [LED Matrix] */
led_cols        = 32;       // columns
led_rows        = 40;       // total rows (5 panels × 8)
led_pitch       = 10;       // mm between LED centers
num_panels      = 5;        // number of 8×32 panels
panel_rows      = 8;        // rows per panel
led_pcb_thick   = 3;        // mm flexible PCB + LEDs

/* [Enclosure] */
wall            = 3;        // mm wall thickness
back            = 2;        // mm back panel thickness
radius          = 8;        // mm corner radius
margin          = 5;        // mm margin around LED area
cavity_depth    = 18;       // mm internal cavity depth

/* [Diffuser] */
diff_thick      = 1.5;      // mm diffuser panel thickness
diff_lip        = 1.5;      // mm lip overlap for seating

/* [Raspberry Pi Pico W] */
pico_l          = 51;       // mm board length
pico_w          = 21;       // mm board width
pico_pcb        = 1.0;      // mm PCB thickness
pico_comp_h     = 3.7;      // mm component height (no USB)
pico_usb_total  = 6.7;      // mm total height with USB connector
pico_usb_w      = 8;        // mm USB connector width
pico_usb_h      = 3;        // mm USB connector height
pico_hole_d     = 2.1;      // mm mounting hole diameter
pico_hole_sp_l  = 47;       // mm hole spacing (length)
pico_hole_sp_w  = 11.4;     // mm hole spacing (width)
standoff_h      = 4;        // mm standoff height
standoff_d      = 5;        // mm standoff outer diameter

/* [DC Barrel Jack] */
barrel_d        = 8;        // mm panel-mount hole diameter

/* [LED Panel Shelf] */
shelf_h         = 8;        // mm height above back panel (wiring clearance)
shelf_t         = 2;        // mm rail/rib wall thickness
chan_bus_w      = 10;       // mm power bus channel width (left, in cross ribs)
chan_inj_w      = 20;       // mm injection wire channel width (center, in cross ribs)
chan_data_w     = 10;       // mm data chain channel width (right, in cross ribs)

/* [Wall Mount - Blind Nail Hole] */
mount_head_d    = 10;       // mm wide entry (nail head)
mount_shaft_d   = 4;        // mm narrow slot (nail shaft)
mount_slot_len  = 8;        // mm slot travel length
mount_depth     = back + shelf_h; // mm total (flush with shelf surface)
mount_floor     = 2;        // mm closed-end thickness (prevents nail perforation)

/* [USB Cutout] */
usb_cut_w       = 14;       // mm width (USB plug + clearance)
usb_cut_h       = 10;       // mm height

/* [Rendering] */
$fn             = 60;

// ================================================================
// DERIVED DIMENSIONS
// ================================================================

led_w       = led_cols * led_pitch;             // 320
led_h       = led_rows * led_pitch;             // 400
pan_h       = panel_rows * led_pitch;           // 80

enc_w       = led_w + 2 * (margin + wall);      // 336
enc_h       = led_h + 2 * (margin + wall);      // 416
enc_d       = back + cavity_depth;              // 20

cav_w       = enc_w - 2 * wall;                 // 330
cav_h       = enc_h - 2 * wall;                 // 410
in_r        = max(1, radius - wall);            // 5

dif_w       = cav_w + 2 * diff_lip;
dif_h       = cav_h + 2 * diff_lip;
dif_r       = in_r + diff_lip;

// Pico W position: bottom-center, USB facing bottom edge
pico_x      = enc_w / 2 - pico_w / 2;
pico_y      = wall + 2;                         // 2mm from inner bottom wall
pico_z      = back;

// LED panel shelf positions
led_x0      = wall + margin;                    // 8 - X start of LED area
led_y0      = wall + margin;                    // 8 - Y start of LED area

// Blind nail mount position: top-center of back panel
mount_x         = enc_w / 2;
mount_y         = enc_h - 28;                   // wide entry Y
mount_boss_h    = mount_depth - back;           // boss protrusion into cavity
mount_cut_depth = mount_depth - mount_floor;    // cut depth (leaves closed floor)

// ================================================================
// PRIMITIVE MODULES
// ================================================================

/// Rounded box from origin corner
/// w, h = footprint; d = extrusion depth; r = corner radius
module rbox(w, h, d, r) {
    hull()
        for (x = [r, w - r], y = [r, h - r])
            translate([x, y, 0])
                cylinder(r = r, h = d);
}

/// Blind mount boss - solid cylinder on interior of back panel
module mount_boss() {
    translate([0, 0, back])
        hull() {
            cylinder(d = mount_head_d + 2 * wall, h = mount_boss_h);
            translate([0, mount_slot_len, 0])
                cylinder(d = mount_shaft_d + 2 * wall, h = mount_boss_h);
        }
}

/// Blind keyhole cut - wide entry at bottom (nail head), narrow rest at top
module mount_cut() {
    cylinder(d = mount_head_d, h = mount_cut_depth);
    translate([-mount_shaft_d / 2, 0, 0])
        cube([mount_shaft_d, mount_slot_len, mount_cut_depth]);
    translate([0, mount_slot_len, 0])
        cylinder(d = mount_shaft_d, h = mount_cut_depth);
}

/// Single mounting standoff with screw hole
/// od = outer diameter; id = inner (screw) hole diameter; h = height
module standoff(od, id, h) {
    difference() {
        cylinder(d = od, h = h);
        translate([0, 0, -0.1])
            cylinder(d = id, h = h + 0.2, $fn = 20);
    }
}

/// Elevated shelf for LED panels (wiring channels underneath for Schema 2)
module led_shelf() {
    // Left perimeter rail (in margin area)
    translate([wall, led_y0, back])
        cube([margin, led_h, shelf_h]);

    // Right perimeter rail (in margin area)
    translate([led_x0 + led_w, led_y0, back])
        cube([margin, led_h, shelf_h]);

    // Bottom edge rail — split for Pico W clearance (center gap)
    pico_gap   = pico_w + 10;
    pico_gap_x = enc_w / 2 - pico_gap / 2;
    translate([wall, wall, back])
        cube([pico_gap_x - wall, margin, shelf_h]);
    translate([pico_gap_x + pico_gap, wall, back])
        cube([wall + cav_w - pico_gap_x - pico_gap, margin, shelf_h]);

    // Top edge rail
    translate([wall, led_y0 + led_h, back])
        cube([cav_w, margin, shelf_h]);

    // Cross ribs between panels (with bus, injection, and data channels)
    for (i = [1 : num_panels - 1]) {
        rib_y   = led_y0 + i * pan_h - shelf_t / 2;
        bus_end = wall + chan_bus_w;
        inj_x0  = enc_w / 2 - chan_inj_w / 2;
        inj_x1  = enc_w / 2 + chan_inj_w / 2;
        data_x0 = led_x0 + led_w + margin - chan_data_w;

        // Segment 1: left solid section — gap on left passes power bus wires
        translate([bus_end, rib_y, back])
            cube([inj_x0 - bus_end, shelf_t, shelf_h]);

        // Segment 2: right solid section — center gap passes injection wires,
        //            gap on right passes data chain wires to next panel
        translate([inj_x1, rib_y, back])
            cube([data_x0 - inj_x1, shelf_t, shelf_h]);
    }

    // Interior Y-direction support ribs (reduced height for wire crossing)
    center_rib_h = shelf_h - 3;
    for (fx = [1/3, 2/3]) {
        rib_x = led_x0 + led_w * fx - shelf_t / 2;
        translate([rib_x, led_y0, back])
            cube([shelf_t, led_h, center_rib_h]);
    }
}

/// LED panel visual model (preview only, not for printing)
module led_panel_visual() {
    color("Black", 0.5)
        cube([led_w, pan_h, led_pcb_thick]);
}

// ================================================================
// ENCLOSURE BODY
// ================================================================

module enclosure() {
    difference() {
        union() {
            // --- Main shell ---
            difference() {
                // --- Outer shell ---
                rbox(enc_w, enc_h, enc_d, radius);

                // --- Inner cavity ---
                translate([wall, wall, back])
                    rbox(cav_w, cav_h, cavity_depth + 1, in_r);

                // --- Diffuser recess (front step) ---
                translate([wall - diff_lip, wall - diff_lip, enc_d - diff_thick])
                    rbox(dif_w, dif_h, diff_thick + 1, dif_r);

                // --- USB cutout (bottom wall, centered on Pico W) ---
                translate([
                    enc_w / 2 - usb_cut_w / 2,
                    -0.5,
                    back + standoff_h - 1
                ])
                    cube([usb_cut_w, wall + 1, usb_cut_h]);

                // --- DC barrel jack hole (bottom wall, offset right) ---
                translate([
                    enc_w / 2 + 50,
                    -0.5,
                    back + cavity_depth / 2
                ])
                    rotate([-90, 0, 0])
                        cylinder(d = barrel_d, h = wall + 1);
            }

            // --- Blind nail mount boss (solid, interior of back panel) ---
            translate([mount_x, mount_y, 0])
                mount_boss();
        }

        // --- Blind nail mount cut (keyhole, closed floor prevents perforation) ---
        translate([mount_x, mount_y, 0])
            mount_cut();
    }

    // --- Pico W mounting standoffs ---
    // dx/dy: offset from board edge to nearest mounting hole center
    translate([pico_x, pico_y, back]) {
        dx = (pico_w - pico_hole_sp_w) / 2;  // 4.8 mm
        dy = (pico_l - pico_hole_sp_l) / 2;  // 2.0 mm
        for (x = [dx, dx + pico_hole_sp_w],
             y = [dy, dy + pico_hole_sp_l])
            translate([x, y, 0])
                standoff(standoff_d, pico_hole_d, standoff_h);
    }

    // --- LED panel shelf (elevated surface with wiring channels) ---
    led_shelf();
}

// ================================================================
// DIFFUSER COVER
// ================================================================

module diffuser() {
    rbox(dif_w, dif_h, diff_thick, dif_r);
}

// ================================================================
// PICO W VISUAL MODEL (preview only, not for printing)
// ================================================================

module pico_visual() {
    // PCB
    color("ForestGreen", 0.8) {
        cube([pico_w, pico_l, pico_pcb]);
        // Components
        translate([2, 5, pico_pcb])
            cube([pico_w - 4, 25, pico_comp_h - pico_pcb]);
        // Wireless module + antenna
        translate([1, 33, pico_pcb])
            cube([pico_w - 2, 14, 2]);
    }
    // USB Micro-B connector (at Y=0 end)
    color("Silver")
        translate([(pico_w - pico_usb_w) / 2, -1.5, 0])
            cube([pico_usb_w, 5, pico_usb_total]);
}

// ================================================================
// ASSEMBLY
// ================================================================

/* [Display] */
show_body       = true;
show_diffuser   = true;
show_pico       = false;
show_panels     = true;
explode         = true;  // set to true to separate diffuser for inspection

ex = explode ? 40 : 0;  // Z offset applied to diffuser when exploded

if (show_body)
    color("DimGray")
        enclosure();

if (show_pico)
    // board surface sits flush on top of standoffs
    translate([pico_x, pico_y, back + standoff_h])
        pico_visual();

if (show_panels)
    // stack 5 panels vertically on top of the shelf surface
    for (i = [0 : num_panels - 1])
        translate([led_x0, led_y0 + i * pan_h, back + shelf_h])
            led_panel_visual();

if (show_diffuser)
    // diffuser seats into front recess; explode lifts it forward for inspection
    translate([
        wall - diff_lip,
        wall - diff_lip,
        enc_d - diff_thick + ex
    ])
        color("White", 0.3)
            diffuser();

// ================================================================
// STL EXPORT HELPERS
// Uncomment ONE at a time, then render (F6) and export STL.
// ================================================================
// enclosure();
// translate([0, 0, diff_thick]) rotate([180, 0, 0]) diffuser();
