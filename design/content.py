"""All the words on the SHEER page: stages, shopping list, links, alerts, notes, sources.
Edit here, then run  python design/build_page.py  to rebuild design/site/index.html."""
from html import escape


def a(href: str, text: str) -> str:
    return f'<a href="{escape(href, quote=True)}" target="_blank" rel="noopener noreferrer">{text}</a>'


# --------------------------------------------------------------------------
# the plan
# --------------------------------------------------------------------------

# (id, title, short description, help html)
STAGES = [
    dict(
        n=0, short="STAGE 0", title="Hold it", meta=["about 2 weeks", "about $60 to $150", "looks-like model"], open=True,
        done="You are holding a see-through, phone-shaped thing and you know whether the size feels right.",
        tasks=[
            ("s0-1", "Pick your colorway", "2 minutes. Tap the colour dots under the phone.",
             "<p>Tap the dots under the phone at the top of the page and tell me your top two in chat. The first print uses your pick.</p>"
             "<p class='tiny'>Tinted resin is the 90s look, so choose a colour you can live with.</p>"),
            ("s0-2", "Get a price for the clear shell", "20 minutes. No buying, just a number.",
             "<ol><li>Grab the two shell files from chat: <span class='mono'>sheer_front_shell.stl</span> and <span class='mono'>sheer_back_shell.stl</span>.</li>"
             f"<li>Open one quote page and upload a file: {a('https://jlc3dp.com/', 'JLC3DP')}, "
             f"{a('https://www.pcbway.com/rapid-prototyping/3d-printing/3d-printing-SLA.html', 'PCBWay SLA printing')} or {a('https://www.xometry.com/', 'Xometry')}.</li>"
             "<li>Choose SLA resin and the transparent or clear material. Quantity 1.</li>"
             "<li>Screenshot the price for both shells and paste it in chat.</li></ol>"
             "<p class='tiny'>PCBWay's own guide recommends their UTR-8100 transparent resin for clear parts.</p>"),
            ("s0-3", "Order the two clear shells", "If the price feels okay. Front shell first is fine.",
             "<p>Pick the cheapest transparent SLA option, one of each shell. If polishing or a clear coat is offered, add it. If tinted clear resin is offered, choose your colour from step 1, otherwise order clear and tint it later.</p>"
             "<p>Allow one to two weeks with shipping. The walls are 2.6 mm thick, which clears the usual 1.2 mm print minimum.</p>"),
            ("s0-4", "Print the dummy guts (optional)", "Screen, board, battery and keyboard board in cheap opaque plastic.",
             "<p>The four <span class='mono'>sheer_dummy_*.stl</span> files are fake parts. Any cheap opaque print works: a friend's printer or a library makerspace is fine. Paint the battery yellow and the board in your colour, then tuck them inside the shells.</p>"),
            ("s0-5", "Buy a used BlackBerry Q10 for feel", "About $30 to $80 on eBay. Any small QWERTY phone works.",
             "<p>Search for a used BlackBerry Q10 on eBay or a local marketplace. You are buying it to learn what good thumb typing feels like and to borrow its key layout. Do not pay extra for pristine.</p>"),
            ("s0-6", "Hold it and write down 3 things to change", "Too thick? Too tall? Wrong keys? Write it down.",
             "<p>Close the shells around the dummy parts, hold it next to the Q10, and write down three things you would change. Send them to me and I will update the model.</p>"),
        ]),
    dict(
        n=1, short="STAGE 1", title="Make the guts work", meta=["4 to 8 weeks", "about $250 to $400", "works-like prototype on Linux"], open=True,
        done="A SIM shows signal, a text arrives, a web page loads over 4G, and sound comes out of a headphone jack.",
        tasks=[
            ("s1-1", "Tell me your country and carrier", "This decides everything about the radio.",
             "<p>Tell me in chat. It decides which 4G bands the modem needs and whether voice calls are realistic where you live. Look for your carrier's page about bringing your own device and about VoLTE.</p>"),
            ("s1-2", "Get a prepaid data + SMS SIM", "Ask whether it works in a hotspot or USB modem.",
             "<p>Pick a cheap prepaid SIM with data and texts. Before buying, ask the carrier whether the SIM works outside a phone (hotspot or modem). Some lock the SIM to a phone's IMEI.</p>"),
            ("s1-3", "Order the Stage 1 parts", "About $250 to $400. The list is further down.",
             "<p>Everything is on the <a href='#shopping'>shopping list</a>. Check each live listing first, and check that Waveshare ships to your country.</p>"),
            ("s1-4", "Flash Raspberry Pi OS and boot with the screen", "An evening. Mostly waiting for downloads.",
             f"<ol><li>Install {a('https://www.raspberrypi.com/software/', 'Raspberry Pi Imager')} on a laptop.</li>"
             "<li>Flash a microSD card with Raspberry Pi OS. Turn on SSH and Wi-Fi in the settings.</li>"
             "<li>Connect the touch display, boot, and see the desktop.</li></ol>"),
            ("s1-5", "Plug in the 4G HAT and see the modem", "The first real win.",
             f"<p>Fit the HAT, insert the SIM, power up, then run <span class='mono'>mmcli -L</span> in a terminal. You want to see a modem listed. Waveshare's {a('https://www.waveshare.com/wiki/SIM7600G-H_4G_HAT_(B)', 'wiki page')} has the connection details and {a('https://modemmanager.org/', 'ModemManager')} is the software.</p>"
             "<p class='tiny'>Nothing shows up? Copy the exact error into chat and we debug it together. I can't touch your hardware, but I can read logs and write fixes.</p>"),
            ("s1-6", "Send a text and load a web page over 4G", "Radio side proven.",
             "<p>Text yourself from the command line (ModemManager's docs show how). Then set up a mobile-data connection with your carrier's APN and open a web page. Both working means the radio is real.</p>"),
            ("s1-7", "Plug in a headset and test both jacks", "This proves the headphone-jack requirement.",
             "<p>Plug headphones into the Pi 4's 3.5 mm jack and play a sound. Then use the headset jack on the 4G HAT for call audio tests.</p>"),
            ("s1-8", "Try a voice call (it might not work)", "A carrier policy can block it. Not your fault.",
             "<p>Place a call with AT commands through the HAT. If your carrier requires VoLTE approval for unknown devices it may be refused. Read Bullshit Alert 3 and move on if so.</p>"),
            ("s1-9", "Type on a mini QWERTY and pick your layout", "Which keys do you reach for that aren't there?",
             "<p>Use any USB mini keyboard to try the layout from the model: four rows, ten keys wide, a D-pad, call and end keys. Note what is missing.</p>"),
        ]),
    dict(
        n=2, short="STAGE 2", title="Squish it together", meta=["2 to 3 months", "about $800 to $2,000", "first carryable prototype"], open=False,
        done="A battery-powered prototype lives inside your own shell and survives a day in your bag.",
        tasks=[
            ("s2-1", "Design the keyboard board in KiCad", "The most beginner-friendly custom board you will ever make.",
             f"<p>Follow {a('https://wiki.ai03.com/', 'ai03\'s PCB Designer Guide')} for the key matrix and {a('https://kicad.org/', 'KiCad')} for the layout. Our key positions are in <span class='mono'>design/art.py</span> and the CAD file.</p>"),
            ("s2-2", "Order 5 keyboard boards", "Five is cheap. Pick a fun solder mask colour.",
             f"<p>Upload the files to {a('https://jlcpcb.com/', 'JLCPCB')}, {a('https://www.pcbway.com/', 'PCBWay')} or {a('https://oshpark.com/', 'OSH Park')}.</p>"),
            ("s2-3", "Flash QMK so it types into the Pi", "QMK makes the board a normal keyboard.",
             f"<p>Start with the {a('https://docs.qmk.fm/', 'QMK docs')}.</p>"),
            ("s2-4", "Swap to a battery-friendly brain with a LiPo and charger", "Pi Zero 2 W class, or a compute module.",
             "<p>The Pi 4 is a desk board. Move to something small and low-power, add a protected LiPo cell and a charger board. I will help pick parts once Stage 1 works.</p>"),
            ("s2-5", "Measure the real parts and update the CAD numbers", "Calipers out.",
             "<p>Measure the real display, board and battery and tell me the numbers. I update <span class='mono'>cad/sheer_v01.py</span> and regenerate the shell.</p>"),
            ("s2-6", "Print shell v0.2 and fit everything inside", "Screw it shut.", "<p>Same process as Stage 0 with the new shell files.</p>"),
            ("s2-7", "Carry it for a day, show five friends, start an email list", "Write down what they touch first.", "<p>The email list matters later for pre-orders. Collect it now while people are excited.</p>"),
        ]),
    dict(
        n=3, short="STAGE 3", title="Your own mainboard", meta=["4 to 8 months", "about $5,000 to $20,000", "engineering build"], open=False,
        done="One custom mainboard boots, connects to the network and fits the shell.",
        tasks=[
            ("s3-1", "Choose a Linux module or an Android module for v1", "I would start with Linux.",
             f"<p>Linux: a Pi-style compute module or similar. Android: a smart module such as {a('https://www.quectel.com/product/lte-sc200r-smart-module-series', 'Quectel\'s SC200R series')} (Android 10, 4G, GPS and Wi-Fi in a 40 mm square). Start Linux unless you have a launch partner.</p>"),
            ("s3-2", "Get dev kits and datasheets", "Expect to talk to a sales rep.", "<p>Module makers usually sell through distributors and want a business conversation for the software package.</p>"),
            ("s3-3", "Pay a hardware engineer to review power, radio and antenna", "A few hours can save months.", "<p>Ask in open-hardware communities or hire a freelancer for a fixed-scope review of your schematic and layout.</p>"),
            ("s3-4", "Design the mainboard and order 5 to 20 assembled boards", "JLCPCB and PCBWay both assemble.", "<p>Small-batch assembly is cheap compared with how much it teaches you.</p>"),
            ("s3-5", "Get tooling quotes and test with urethane casting first", "Two moulders, same file.", "<p>Ask for aluminium tool pricing and the extra cost of a polished clear or tinted finish.</p>"),
        ]),
    dict(
        n=4, short="STAGE 4", title="Make it legal, then sell it", meta=["6 to 12+ months", "$30,000 to $100,000+ (very rough)", "certification and production"], open=False,
        done="Test labs pass it, a factory builds it, and someone who isn't your friend buys it.",
        tasks=[
            ("s4-1", "Pick launch countries and get lab quotes", "FCC, CE, UKCA or RCM, plus SAR, battery and carrier tests.", "<p>Pre-certified radio modules cut part of this, but the finished phone still needs its own testing.</p>"),
            ("s4-2", "Trademark search, company, insurance", "Check the name before you print it on anything.", "<p>SHEER is a working title. Search trademarks in your launch countries before committing.</p>"),
            ("s4-3", "Run pre-orders or a campaign", "Only after it works.", f"<p>{a('https://www.crowdsupply.com/apply', 'Crowd Supply')} is built for open hardware and handles fulfilment. Kickstarter and Tindie are the other usual routes.</p>"),
            ("s4-4", "Pick a contract manufacturer and run a pilot batch", "50 to 200 units.", "<p>A pilot run finds the problems that one hand-built prototype never shows.</p>"),
        ]),
]

# --------------------------------------------------------------------------
# shopping list: (part, why, price, (href, label) or None)
# --------------------------------------------------------------------------
SHOP = [
    ("Raspberry Pi 4 Model B (2 to 4 GB)", "A real 3.5 mm audio jack, the screen port, and the most tutorials. The Pi 5 dropped the jack.", "$45 to $60", ("https://www.raspberrypi.com/products/raspberry-pi-4-model-b/", "Raspberry Pi")),
    ("Raspberry Pi Touch Display 2 (5 inch)", "720 × 1280 touchscreen in portrait, like a phone. Ribbon cable, no extra power.", "$58 to $64", ("https://www.adafruit.com/product/6408", "Adafruit")),
    ("Waveshare SIM7600G-H 4G HAT (B)", "Global-band 4G modem with GPS, a SIM slot and its own audio jack for call tests.", "check price", ("https://www.waveshare.com/product/iot-communication/long-range-wireless/4g-gsm-gprs/sim7600g-h-4g-hat-b.htm", "Waveshare")),
    ("microSD card, 32 GB", "The Pi's boot drive.", "$8 to $12", None),
    ("USB-C power supply, 5 V 3 A", "The Pi 4 draws up to 3 A. A weak charger causes weird glitches.", "$12 to $20", None),
    ("Prepaid data + SMS SIM", "For texts and data. Ask whether it works outside a phone.", "$10 to $15 a month", None),
    ("Headset with mic (3.5 mm)", "Tests the jack and call audio.", "$8 to $15", None),
    ("USB mini keyboard", "A typing test before you build your own.", "$10 to $20", None),
    ("Used BlackBerry Q10", "The feel reference for thumb typing.", "$30 to $80", None),
    ("Digital calipers", "Measure real parts for model v0.2.", "$15 to $25", None),
]

# --------------------------------------------------------------------------
# link cards
# --------------------------------------------------------------------------
LINKS = [
    ("Design and CAD", [
        ("https://kicad.org/", "KiCad", "Free circuit-board design."),
        ("https://www.onshape.com/", "Onshape", "CAD that runs in a browser."),
        ("https://www.autodesk.com/products/fusion-360/blog/fusion-for-personal-use-vs-autodesk-fusion/", "Fusion for personal use", "Free for hobby projects. You need a paid or startup licence once you sell."),
        ("https://www.freecad.org/", "FreeCAD", "Free and open-source CAD."),
        ("https://cadquery.readthedocs.io/", "CadQuery", "The Python tool behind the model in this repo."),
        ("https://www.blender.org/", "Blender", "Pretty renders and organic shapes."),
    ]),
    ("Clear 3D printing", [
        ("https://jlc3dp.com/", "JLC3DP", "SLA with transparent resin, instant quotes."),
        ("https://www.pcbway.com/rapid-prototyping/3d-printing/3d-printing-SLA.html", "PCBWay SLA printing", "Accepts STL and STEP up to 50 MB."),
        ("https://learn.adafruit.com/clear-resin-3d-prints-with-pcbway", "Adafruit: clear resin with PCBWay", "Settings that give clear prints."),
        ("https://www.xometry.com/", "Xometry", "Instant quotes, polished clear options."),
        ("https://www.protolabs.com/", "Protolabs", "Pricier and fast. Also does moulding."),
    ]),
    ("Boards: PCB and assembly", [
        ("https://jlcpcb.com/", "JLCPCB", "Cheap boards and assembly."),
        ("https://www.pcbway.com/", "PCBWay", "Boards, assembly, CNC and printing in one place."),
        ("https://oshpark.com/", "OSH Park", "US-made purple boards."),
        ("https://www.seeedstudio.com/", "Seeed Studio", "Small-batch fabrication plus modules."),
    ]),
    ("Parts", [
        ("https://www.digikey.com/", "DigiKey", "Everything, with real datasheets."),
        ("https://www.mouser.com/", "Mouser", "Same idea, different stock."),
        ("https://www.lcsc.com/", "LCSC", "Pairs with JLCPCB assembly."),
        ("https://www.adafruit.com/", "Adafruit", "Friendly breakouts and guides."),
        ("https://www.sparkfun.com/", "SparkFun", "More of the same."),
        ("https://www.waveshare.com/", "Waveshare", "HATs, displays and modems."),
        ("https://shop.pimoroni.com/", "Pimoroni", "UK-based Pi accessories."),
    ]),
    ("Radio and Android modules", [
        ("https://www.quectel.com/product/lte-sc200r-smart-module-series", "Quectel SC200R series", "Android 10 smart module with 4G, GPS, Wi-Fi."),
        ("https://www.quectel.com/", "Quectel", "Modems and smart modules."),
        ("https://www.raspberrypi.com/products/", "Raspberry Pi", "Compute modules and small boards."),
    ]),
    ("Learn the software", [
        ("https://modemmanager.org/", "ModemManager", "How Linux talks to a 4G modem."),
        ("https://postmarketos.org/", "postmarketOS", "Linux for phones."),
        ("https://mobian.org/", "Mobian", "Debian for phones."),
        ("https://waydro.id/", "Waydroid", "Run Android apps on Linux."),
        ("https://docs.qmk.fm/", "QMK docs", "Keyboard firmware."),
        ("https://wiki.ai03.com/", "ai03 PCB guide", "How to design a keyboard board."),
        ("https://www.raspberrypi.com/software/", "Raspberry Pi Imager", "Flash the SD card."),
    ]),
    ("Make it legal", [
        ("https://soracom.io/iot-definitions/what-is-ptcrb/", "What is PTCRB?", "Plain-English carrier certification."),
        ("https://www.digi.com/blog/post/2017/5-myths-about-cellular-carrier-certification", "Digi: 5 myths about carrier certification", "Why a certified module is not a certified product."),
        ("https://bayton.org/blog/2024/01/certifying-android-devices/", "Certifying Android devices", "How Google's licence and testing work."),
    ]),
    ("Sell it", [
        ("https://www.crowdsupply.com/apply", "Crowd Supply", "Open-hardware crowdfunding with fulfilment."),
        ("https://www.kickstarter.com/", "Kickstarter", "The big one."),
        ("https://www.tindie.com/", "Tindie", "Small runs of maker hardware."),
    ]),
    ("Who else is doing this", [
        ("https://9to5google.com/2026/09/18/clicks-communicator-lands-in-december-with-12gb-ram-two-months-of-free-data/", "Clicks Communicator", "Android phone with a real keyboard and a jack."),
        ("https://www.unihertz.com/products/titan-2", "Unihertz Titan 2", "Keyboard phone. No jack on the official page."),
        ("https://www.raspberrypi.com/news/beepberry-cures-lack-of-blackberry/", "Beepberry", "Pi Zero with a BlackBerry keyboard."),
        ("https://www.hackster.io/news/the-zerophone-a-linux-smartphone-powered-by-the-raspberry-pi-zero-286f36a25fd4", "ZeroPhone", "An earlier DIY Pi phone."),
        ("https://forum.clockworkpi.com/t/uconsole-4g-lte/20765", "uConsole 4G", "Linux handheld with a keyboard and optional 4G."),
    ]),
]

# --------------------------------------------------------------------------
# alerts
# --------------------------------------------------------------------------
ALERTS = [
    ("Clear plastic is not free glamour",
     "Every wire, glue blob and logo sticker is on show, and perfectly clear plastic looks cheap fast. All the old gear you sent is <b>tinted</b> translucent. Pick a tint, design the guts to look good, and treat the battery label like artwork."),
    ("Android on your own hardware is hard mode",
     "You need a chip maker's board package, and the Play Store needs Google's licence plus device testing, which sources put at months. <b>Start on Linux</b>, use Waydroid for Android apps, and revisit Android modules at Stage 3."),
    ("Calls may be refused in your country",
     "Some carriers only let approved phones place voice calls over 4G (VoLTE). PinePhone owners hit this in the US in 2021. <b>Get text and data working first</b>, then ask your carrier, or a reseller that doesn't care what device you use."),
    ("2G and 3G modules are dead ends",
     "Cheap GSM boards look tempting, but 2G and 3G networks are closing in many countries. <b>Buy 4G LTE.</b> The first ZeroPhone started on 2G, which is charming history and a bad plan."),
    ("Selling a radio needs paperwork",
     "Rough figures from vendor blogs: FCC testing in the thousands, PTCRB around $10k to $50k, plus lab time for the whole phone. A pre-certified module helps but <b>does not certify your finished phone</b>. Building one for yourself needs none of this. Also, don't take pre-orders until a prototype works."),
    ("The software is most of the work",
     "Sleep and wake, modem state, audio routing and battery life are where phones fall apart. <b>Budget more time for software than hardware.</b> This is the part I can help with the most."),
    ("Lithium batteries in clear cases show their feelings",
     "A swelling pouch cell is visible from outside. Use a protected cell, keep screws away from it, and know that shipping batteries has its own rules (UN38.3). <b>Never puncture or squeeze it.</b>"),
    ("Tooling is the big first bill",
     "A simple prototype mould can start around $1,500, but forum and vendor estimates put a polished, tinted two-part phone shell at $10k to $50k. Get quotes from two moulders <b>before</b> you fall in love with a shape."),
]

# --------------------------------------------------------------------------
# design notes
# --------------------------------------------------------------------------
NOTES = [
    ("Tinted, never fully clear", "Real 90s see-through gear is tinted. A tint hides some mess and makes the guts look intentional."),
    ("The guts are the artwork", "A coloured circuit board with gold pads, a yellow battery label and four chrome screws. We design the board to be looked at."),
    ("Jelly keys that glow", "Backlit keys bleed colour through clear keycaps, and the notification light glows through the plastic."),
    ("Square screen, BlackBerry style", "A 56 × 56 mm window leaves room for a roomier keyboard. Fewer pixels, more thumb comfort."),
    ("Headphone jack on top", "With a tiny printed headphones glyph, like a Walkman. A headset-capable jack, so mics work too."),
    ("Visible screws, repairable", "Four screws and no glue. Repairable is a selling point, and it looks right on see-through tech."),
    ("A pet in the status bar", "A small Tamagotchi-style pet that reacts to battery and typing. Cheap software, great for screenshots."),
    ("Swap-on jelly backs, later", "90s phones had snap-on covers. Selling extra backs is merch money for version 0.2."),
]

# --------------------------------------------------------------------------
# sources shown in the footer (url, label)
# --------------------------------------------------------------------------
SOURCES = [
    ("https://9to5google.com/2026/09/18/clicks-communicator-lands-in-december-with-12gb-ram-two-months-of-free-data/", "9to5Google: Clicks Communicator ships in December"),
    ("https://www.unihertz.com/products/titan-2", "Unihertz: Titan 2 product page (lists no 3.5 mm jack)"),
    ("https://forum.pine64.org/printthread.php?tid=19795", "Pine64 forum: PinePhone keyboard case out of stock"),
    ("https://www.raspberrypi.com/news/beepberry-cures-lack-of-blackberry/", "Raspberry Pi news: Beepberry"),
    ("https://circuitpython.org/board/solderparty_bbq20kbd/", "CircuitPython: Solder Party BBQ20KBD keyboard"),
    ("https://www.quectel.com/product/lte-sc200r-smart-module-series", "Quectel: SC200R smart module series"),
    ("https://learn.adafruit.com/clear-resin-3d-prints-with-pcbway", "Adafruit: clear resin prints with PCBWay"),
    ("https://www.crowdsupply.com/apply", "Crowd Supply: how campaigns work"),
    ("https://soracom.io/iot-definitions/what-is-ptcrb/", "Soracom: what is PTCRB"),
    ("https://www.digi.com/blog/post/2017/5-myths-about-cellular-carrier-certification", "Digi: 5 myths about cellular carrier certification"),
    ("https://bayton.org/blog/2024/01/certifying-android-devices/", "Bayton: certifying Android devices"),
    ("https://forum.pine64.org/showthread.php?tid=12897", "Pine64 forum: PinePhone refused on a US carrier (VoLTE whitelists)"),
    ("https://www.waveshare.com/product/iot-communication/long-range-wireless/4g-gsm-gprs/sim7600g-h-4g-hat-b.htm", "Waveshare: SIM7600G-H 4G HAT (B)"),
    ("https://www.adafruit.com/product/6408", "Adafruit: Raspberry Pi Touch Display 2, 5 inch"),
    ("https://www.autodesk.com/products/fusion-360/blog/fusion-for-personal-use-vs-autodesk-fusion/", "Autodesk: Fusion for personal use"),
    ("https://www.hackster.io/news/the-zerophone-a-linux-smartphone-powered-by-the-raspberry-pi-zero-286f36a25fd4", "Hackster: ZeroPhone"),
    ("https://forum.clockworkpi.com/t/uconsole-4g-lte/20765", "ClockworkPi forum: uConsole 4G"),
    ("https://www.engineering.com/?p=17283", "Engineering.com: low-volume injection moulding costs"),
]
