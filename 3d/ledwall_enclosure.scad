/*
 * Ledwall Enclosure - Prototype v1
 *
 * Parametric enclosure for 40x32 WS2812B LED wall
 * with Raspberry Pi Pico W controller.
 *
 * Setup:
 *   5x 8x32 flexible LED matrix panels (10mm pitch)
 *   stacked vertically → 40 rows × 32 cols
 *   Raspberry Pi Pico W controller (bottom rear)
 *   DC barrel jack 5.5×2.1mm power input
 *   Wall-mounted via keyhole slots
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

/* [Wall Mount Keyholes] */
key_wide        = 10;       // mm wide part (screw head entry)
key_narrow      = 5;        // mm narrow part (screw shaft)
key_slot        = 8;        // mm slot length

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

// ================================================================
// PRIMITIVE MODULES
// ================================================================

/// Rounded box from origin corner
module rbox(w, h, d, r) {
    hull()
        for (x = [r, w - r], y = [r, h - r])
            translate([x, y, 0])
                cylinder(r = r, h = d);
}

/// Keyhole wall-mount slot (screw head enters wide, slides into narrow)
module keyhole(wd, nw, sl, th) {
    cylinder(d = wd, h = th);
    translate([-nw / 2, 0, 0])
        cube([nw, sl, th]);
    translate([0, sl, 0])
        cylinder(d = nw, h = th);
}

/// Single mounting standoff with screw hole
module standoff(od, id, h) {
    difference() {
        cylinder(d = od, h = h);
        translate([0, 0, -0.1])
            cylinder(d = id, h = h + 0.2, $fn = 20);
    }
}

// ================================================================
// ENCLOSURE BODY
// ================================================================

module enclosure() {
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

        // --- Wall-mount keyholes (back panel) ---
        // Two at top corners
        for (sx = [-1, 1])
            translate([
                enc_w / 2 + sx * (enc_w / 2 - 30),
                enc_h - 40,
                -0.5
            ])
                keyhole(key_wide, key_narrow, key_slot, back + 1);

        // One at bottom center
        translate([enc_w / 2, 40, -0.5])
            keyhole(key_wide, key_narrow, key_slot, back + 1);
    }

    // --- Pico W mounting standoffs ---
    translate([pico_x, pico_y, back]) {
        dx = (pico_w - pico_hole_sp_w) / 2;
        dy = (pico_l - pico_hole_sp_l) / 2;
        for (x = [dx, dx + pico_hole_sp_w],
             y = [dy, dy + pico_hole_sp_l])
            translate([x, y, 0])
                standoff(standoff_d, pico_hole_d, standoff_h);
    }

    // --- LED panel alignment ribs (between panels) ---
    for (i = [1 : num_panels - 1])
        translate([
            wall + margin,
            wall + margin + i * pan_h - 1,
            back
        ])
            cube([led_w, 2, 3]);
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
show_pico       = true;
explode         = false;

ex = explode ? 40 : 0;

if (show_body)
    color("DimGray")
        enclosure();

if (show_pico)
    translate([pico_x, pico_y, back + standoff_h])
        pico_visual();

if (show_diffuser)
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
