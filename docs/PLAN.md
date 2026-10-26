# SHEER: the plan

_Generated from `design/content.py` by `design/build_page.py`. Edit the content file, not this one._

Five stages. Do one small thing at a time. Money and time are rough ballparks, not quotes.

## Stage 0: Hold it

about 2 weeks · about $60 to $150 · looks-like model

**Done when:** You are holding a see-through, phone-shaped thing and you know whether the size feels right.

- [ ] **Pick your colorway**. 2 minutes. Tap the colour dots under the phone.
  Tap the dots under the phone at the top of the page and tell me your top two in chat. The first print uses your pick.

  Tinted resin is the 90s look, so choose a colour you can live with.
- [ ] **Get a price for the clear shell**. 20 minutes. No buying, just a number.
  - Grab the two shell files from chat: `sheer_front_shell.stl` and `sheer_back_shell.stl`.
  - Open one quote page and upload a file: [JLC3DP](https://jlc3dp.com/), [PCBWay SLA printing](https://www.pcbway.com/rapid-prototyping/3d-printing/3d-printing-SLA.html) or [Xometry](https://www.xometry.com/).
  - Choose SLA resin and the transparent or clear material. Quantity 1.
  - Screenshot the price for both shells and paste it in chat.

  PCBWay's own guide recommends their UTR-8100 transparent resin for clear parts.
- [ ] **Order the two clear shells**. If the price feels okay. Front shell first is fine.
  Pick the cheapest transparent SLA option, one of each shell. If polishing or a clear coat is offered, add it. If tinted clear resin is offered, choose your colour from step 1, otherwise order clear and tint it later.

  Allow one to two weeks with shipping. The walls are 2.6 mm thick, which clears the usual 1.2 mm print minimum.
- [ ] **Print the dummy guts (optional)**. Screen, board, battery and keyboard board in cheap opaque plastic.
  The four `sheer_dummy_*.stl` files are fake parts. Any cheap opaque print works: a friend's printer or a library makerspace is fine. Paint the battery yellow and the board in your colour, then tuck them inside the shells.
- [ ] **Buy a used BlackBerry Q10 for feel**. About $30 to $80 on eBay. Any small QWERTY phone works.
  Search for a used BlackBerry Q10 on eBay or a local marketplace. You are buying it to learn what good thumb typing feels like and to borrow its key layout. Do not pay extra for pristine.
- [ ] **Hold it and write down 3 things to change**. Too thick? Too tall? Wrong keys? Write it down.
  Close the shells around the dummy parts, hold it next to the Q10, and write down three things you would change. Send them to me and I will update the model.

## Stage 1: Make the guts work

4 to 8 weeks · about $250 to $400 · works-like prototype on Linux

**Done when:** A SIM shows signal, a text arrives, a web page loads over 4G, and sound comes out of a headphone jack.

- [ ] **Tell me your country and carrier**. This decides everything about the radio.
  Tell me in chat. It decides which 4G bands the modem needs and whether voice calls are realistic where you live. Look for your carrier's page about bringing your own device and about VoLTE.
- [ ] **Get a prepaid data + SMS SIM**. Ask whether it works in a hotspot or USB modem.
  Pick a cheap prepaid SIM with data and texts. Before buying, ask the carrier whether the SIM works outside a phone (hotspot or modem). Some lock the SIM to a phone's IMEI.
- [ ] **Order the Stage 1 parts**. About $250 to $400. The list is further down.
  Everything is on the shopping list below. Check each live listing first, and check that Waveshare ships to your country.
- [ ] **Flash Raspberry Pi OS and boot with the screen**. An evening. Mostly waiting for downloads.
  - Install [Raspberry Pi Imager](https://www.raspberrypi.com/software/) on a laptop.
  - Flash a microSD card with Raspberry Pi OS. Turn on SSH and Wi-Fi in the settings.
  - Connect the touch display, boot, and see the desktop.
- [ ] **Plug in the 4G HAT and see the modem**. The first real win.
  Fit the HAT, insert the SIM, power up, then run `mmcli -L` in a terminal. You want to see a modem listed. Waveshare's [wiki page](https://www.waveshare.com/wiki/SIM7600G-H_4G_HAT_(B)) has the connection details and [ModemManager](https://modemmanager.org/) is the software.

  Nothing shows up? Copy the exact error into chat and we debug it together. I can't touch your hardware, but I can read logs and write fixes.
- [ ] **Send a text and load a web page over 4G**. Radio side proven.
  Text yourself from the command line (ModemManager's docs show how). Then set up a mobile-data connection with your carrier's APN and open a web page. Both working means the radio is real.
- [ ] **Plug in a headset and test both jacks**. This proves the headphone-jack requirement.
  Plug headphones into the Pi 4's 3.5 mm jack and play a sound. Then use the headset jack on the 4G HAT for call audio tests.
- [ ] **Try a voice call (it might not work)**. A carrier policy can block it. Not your fault.
  Place a call with AT commands through the HAT. If your carrier requires VoLTE approval for unknown devices it may be refused. Read Bullshit Alert 3 and move on if so.
- [ ] **Type on a mini QWERTY and pick your layout**. Which keys do you reach for that aren't there?
  Use any USB mini keyboard to try the layout from the model: four rows, ten keys wide, a D-pad, call and end keys. Note what is missing.

## Stage 2: Squish it together

2 to 3 months · about $800 to $2,000 · first carryable prototype

**Done when:** A battery-powered prototype lives inside your own shell and survives a day in your bag.

- [ ] **Design the keyboard board in KiCad**. The most beginner-friendly custom board you will ever make.
  Follow [ai03's PCB Designer Guide](https://wiki.ai03.com/) for the key matrix and [KiCad](https://kicad.org/) for the layout. Our key positions are in `design/art.py` and the CAD file.
- [ ] **Order 5 keyboard boards**. Five is cheap. Pick a fun solder mask colour.
  Upload the files to [JLCPCB](https://jlcpcb.com/), [PCBWay](https://www.pcbway.com/) or [OSH Park](https://oshpark.com/).
- [ ] **Flash QMK so it types into the Pi**. QMK makes the board a normal keyboard.
  Start with the [QMK docs](https://docs.qmk.fm/).
- [ ] **Swap to a battery-friendly brain with a LiPo and charger**. Pi Zero 2 W class, or a compute module.
  The Pi 4 is a desk board. Move to something small and low-power, add a protected LiPo cell and a charger board. I will help pick parts once Stage 1 works.
- [ ] **Measure the real parts and update the CAD numbers**. Calipers out.
  Measure the real display, board and battery and tell me the numbers. I update `cad/sheer_v01.py` and regenerate the shell.
- [ ] **Print shell v0.2 and fit everything inside**. Screw it shut.
  Same process as Stage 0 with the new shell files.
- [ ] **Carry it for a day, show five friends, start an email list**. Write down what they touch first.
  The email list matters later for pre-orders. Collect it now while people are excited.

## Stage 3: Your own mainboard

4 to 8 months · about $5,000 to $20,000 · engineering build

**Done when:** One custom mainboard boots, connects to the network and fits the shell.

- [ ] **Choose a Linux module or an Android module for v1**. I would start with Linux.
  Linux: a Pi-style compute module or similar. Android: a smart module such as [Quectel's SC200R series](https://www.quectel.com/product/lte-sc200r-smart-module-series) (Android 10, 4G, GPS and Wi-Fi in a 40 mm square). Start Linux unless you have a launch partner.
- [ ] **Get dev kits and datasheets**. Expect to talk to a sales rep.
  Module makers usually sell through distributors and want a business conversation for the software package.
- [ ] **Pay a hardware engineer to review power, radio and antenna**. A few hours can save months.
  Ask in open-hardware communities or hire a freelancer for a fixed-scope review of your schematic and layout.
- [ ] **Design the mainboard and order 5 to 20 assembled boards**. JLCPCB and PCBWay both assemble.
  Small-batch assembly is cheap compared with how much it teaches you.
- [ ] **Get tooling quotes and test with urethane casting first**. Two moulders, same file.
  Ask for aluminium tool pricing and the extra cost of a polished clear or tinted finish.

## Stage 4: Make it legal, then sell it

6 to 12+ months · $30,000 to $100,000+ (very rough) · certification and production

**Done when:** Test labs pass it, a factory builds it, and someone who isn't your friend buys it.

- [ ] **Pick launch countries and get lab quotes**. FCC, CE, UKCA or RCM, plus SAR, battery and carrier tests.
  Pre-certified radio modules cut part of this, but the finished phone still needs its own testing.
- [ ] **Trademark search, company, insurance**. Check the name before you print it on anything.
  SHEER is a working title. Search trademarks in your launch countries before committing.
- [ ] **Run pre-orders or a campaign**. Only after it works.
  [Crowd Supply](https://www.crowdsupply.com/apply) is built for open hardware and handles fulfilment. Kickstarter and Tindie are the other usual routes.
- [ ] **Pick a contract manufacturer and run a pilot batch**. 50 to 200 units.
  A pilot run finds the problems that one hand-built prototype never shows.

## Stage 1 shopping list

| Part | Why | About | Link |
|---|---|---|---|
| Raspberry Pi 4 Model B (2 to 4 GB) | A real 3.5 mm audio jack, the screen port, and the most tutorials. The Pi 5 dropped the jack. | $45 to $60 | [Raspberry Pi](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) |
| Raspberry Pi Touch Display 2 (5 inch) | 720 × 1280 touchscreen in portrait, like a phone. Ribbon cable, no extra power. | $58 to $64 | [Adafruit](https://www.adafruit.com/product/6408) |
| Waveshare SIM7600G-H 4G HAT (B) | Global-band 4G modem with GPS, a SIM slot and its own audio jack for call tests. | check price | [Waveshare](https://www.waveshare.com/product/iot-communication/long-range-wireless/4g-gsm-gprs/sim7600g-h-4g-hat-b.htm) |
| microSD card, 32 GB | The Pi's boot drive. | $8 to $12 | any shop |
| USB-C power supply, 5 V 3 A | The Pi 4 draws up to 3 A. A weak charger causes weird glitches. | $12 to $20 | any shop |
| Prepaid data + SMS SIM | For texts and data. Ask whether it works outside a phone. | $10 to $15 a month | any shop |
| Headset with mic (3.5 mm) | Tests the jack and call audio. | $8 to $15 | any shop |
| USB mini keyboard | A typing test before you build your own. | $10 to $20 | any shop |
| Used BlackBerry Q10 | The feel reference for thumb typing. | $30 to $80 | any shop |
| Digital calipers | Measure real parts for model v0.2. | $15 to $25 | any shop |

Prices are rough guesses. Check the live listing.

## Websites for every stage

**Design and CAD**
- [KiCad](https://kicad.org/): Free circuit-board design.
- [Onshape](https://www.onshape.com/): CAD that runs in a browser.
- [Fusion for personal use](https://www.autodesk.com/products/fusion-360/blog/fusion-for-personal-use-vs-autodesk-fusion/): Free for hobby projects. You need a paid or startup licence once you sell.
- [FreeCAD](https://www.freecad.org/): Free and open-source CAD.
- [CadQuery](https://cadquery.readthedocs.io/): The Python tool behind the model in this repo.
- [Blender](https://www.blender.org/): Pretty renders and organic shapes.

**Clear 3D printing**
- [JLC3DP](https://jlc3dp.com/): SLA with transparent resin, instant quotes.
- [PCBWay SLA printing](https://www.pcbway.com/rapid-prototyping/3d-printing/3d-printing-SLA.html): Accepts STL and STEP up to 50 MB.
- [Adafruit: clear resin with PCBWay](https://learn.adafruit.com/clear-resin-3d-prints-with-pcbway): Settings that give clear prints.
- [Xometry](https://www.xometry.com/): Instant quotes, polished clear options.
- [Protolabs](https://www.protolabs.com/): Pricier and fast. Also does moulding.

**Boards: PCB and assembly**
- [JLCPCB](https://jlcpcb.com/): Cheap boards and assembly.
- [PCBWay](https://www.pcbway.com/): Boards, assembly, CNC and printing in one place.
- [OSH Park](https://oshpark.com/): US-made purple boards.
- [Seeed Studio](https://www.seeedstudio.com/): Small-batch fabrication plus modules.

**Parts**
- [DigiKey](https://www.digikey.com/): Everything, with real datasheets.
- [Mouser](https://www.mouser.com/): Same idea, different stock.
- [LCSC](https://www.lcsc.com/): Pairs with JLCPCB assembly.
- [Adafruit](https://www.adafruit.com/): Friendly breakouts and guides.
- [SparkFun](https://www.sparkfun.com/): More of the same.
- [Waveshare](https://www.waveshare.com/): HATs, displays and modems.
- [Pimoroni](https://shop.pimoroni.com/): UK-based Pi accessories.

**Radio and Android modules**
- [Quectel SC200R series](https://www.quectel.com/product/lte-sc200r-smart-module-series): Android 10 smart module with 4G, GPS, Wi-Fi.
- [Quectel](https://www.quectel.com/): Modems and smart modules.
- [Raspberry Pi](https://www.raspberrypi.com/products/): Compute modules and small boards.

**Learn the software**
- [ModemManager](https://modemmanager.org/): How Linux talks to a 4G modem.
- [postmarketOS](https://postmarketos.org/): Linux for phones.
- [Mobian](https://mobian.org/): Debian for phones.
- [Waydroid](https://waydro.id/): Run Android apps on Linux.
- [QMK docs](https://docs.qmk.fm/): Keyboard firmware.
- [ai03 PCB guide](https://wiki.ai03.com/): How to design a keyboard board.
- [Raspberry Pi Imager](https://www.raspberrypi.com/software/): Flash the SD card.

**Make it legal**
- [What is PTCRB?](https://soracom.io/iot-definitions/what-is-ptcrb/): Plain-English carrier certification.
- [Digi: 5 myths about carrier certification](https://www.digi.com/blog/post/2017/5-myths-about-cellular-carrier-certification): Why a certified module is not a certified product.
- [Certifying Android devices](https://bayton.org/blog/2024/01/certifying-android-devices/): How Google's licence and testing work.

**Sell it**
- [Crowd Supply](https://www.crowdsupply.com/apply): Open-hardware crowdfunding with fulfilment.
- [Kickstarter](https://www.kickstarter.com/): The big one.
- [Tindie](https://www.tindie.com/): Small runs of maker hardware.

**Who else is doing this**
- [Clicks Communicator](https://9to5google.com/2026/09/18/clicks-communicator-lands-in-december-with-12gb-ram-two-months-of-free-data/): Android phone with a real keyboard and a jack.
- [Unihertz Titan 2](https://www.unihertz.com/products/titan-2): Keyboard phone. No jack on the official page.
- [Beepberry](https://www.raspberrypi.com/news/beepberry-cures-lack-of-blackberry/): Pi Zero with a BlackBerry keyboard.
- [ZeroPhone](https://www.hackster.io/news/the-zerophone-a-linux-smartphone-powered-by-the-raspberry-pi-zero-286f36a25fd4): An earlier DIY Pi phone.
- [uConsole 4G](https://forum.clockworkpi.com/t/uconsole-4g-lte/20765): Linux handheld with a keyboard and optional 4G.

## Bullshit alerts

1. **Clear plastic is not free glamour.** Every wire, glue blob and logo sticker is on show, and perfectly clear plastic looks cheap fast. All the old gear you sent is **tinted** translucent. Pick a tint, design the guts to look good, and treat the battery label like artwork.
2. **Android on your own hardware is hard mode.** You need a chip maker's board package, and the Play Store needs Google's licence plus device testing, which sources put at months. **Start on Linux**, use Waydroid for Android apps, and revisit Android modules at Stage 3.
3. **Calls may be refused in your country.** Some carriers only let approved phones place voice calls over 4G (VoLTE). PinePhone owners hit this in the US in 2021. **Get text and data working first**, then ask your carrier, or a reseller that doesn't care what device you use.
4. **2G and 3G modules are dead ends.** Cheap GSM boards look tempting, but 2G and 3G networks are closing in many countries. **Buy 4G LTE.** The first ZeroPhone started on 2G, which is charming history and a bad plan.
5. **Selling a radio needs paperwork.** Rough figures from vendor blogs: FCC testing in the thousands, PTCRB around $10k to $50k, plus lab time for the whole phone. A pre-certified module helps but **does not certify your finished phone**. Building one for yourself needs none of this. Also, don't take pre-orders until a prototype works.
6. **The software is most of the work.** Sleep and wake, modem state, audio routing and battery life are where phones fall apart. **Budget more time for software than hardware.** This is the part I can help with the most.
7. **Lithium batteries in clear cases show their feelings.** A swelling pouch cell is visible from outside. Use a protected cell, keep screws away from it, and know that shipping batteries has its own rules (UN38.3). **Never puncture or squeeze it.**
8. **Tooling is the big first bill.** A simple prototype mould can start around $1,500, but forum and vendor estimates put a polished, tinted two-part phone shell at $10k to $50k. Get quotes from two moulders **before** you fall in love with a shape.

## Sources

- [9to5Google: Clicks Communicator ships in December](https://9to5google.com/2026/09/18/clicks-communicator-lands-in-december-with-12gb-ram-two-months-of-free-data/)
- [Unihertz: Titan 2 product page (lists no 3.5 mm jack)](https://www.unihertz.com/products/titan-2)
- [Pine64 forum: PinePhone keyboard case out of stock](https://forum.pine64.org/printthread.php?tid=19795)
- [Raspberry Pi news: Beepberry](https://www.raspberrypi.com/news/beepberry-cures-lack-of-blackberry/)
- [CircuitPython: Solder Party BBQ20KBD keyboard](https://circuitpython.org/board/solderparty_bbq20kbd/)
- [Quectel: SC200R smart module series](https://www.quectel.com/product/lte-sc200r-smart-module-series)
- [Adafruit: clear resin prints with PCBWay](https://learn.adafruit.com/clear-resin-3d-prints-with-pcbway)
- [Crowd Supply: how campaigns work](https://www.crowdsupply.com/apply)
- [Soracom: what is PTCRB](https://soracom.io/iot-definitions/what-is-ptcrb/)
- [Digi: 5 myths about cellular carrier certification](https://www.digi.com/blog/post/2017/5-myths-about-cellular-carrier-certification)
- [Bayton: certifying Android devices](https://bayton.org/blog/2024/01/certifying-android-devices/)
- [Pine64 forum: PinePhone refused on a US carrier (VoLTE whitelists)](https://forum.pine64.org/showthread.php?tid=12897)
- [Waveshare: SIM7600G-H 4G HAT (B)](https://www.waveshare.com/product/iot-communication/long-range-wireless/4g-gsm-gprs/sim7600g-h-4g-hat-b.htm)
- [Adafruit: Raspberry Pi Touch Display 2, 5 inch](https://www.adafruit.com/product/6408)
- [Autodesk: Fusion for personal use](https://www.autodesk.com/products/fusion-360/blog/fusion-for-personal-use-vs-autodesk-fusion/)
- [Hackster: ZeroPhone](https://www.hackster.io/news/the-zerophone-a-linux-smartphone-powered-by-the-raspberry-pi-zero-286f36a25fd4)
- [ClockworkPi forum: uConsole 4G](https://forum.clockworkpi.com/t/uconsole-4g-lte/20765)
- [Engineering.com: low-volume injection moulding costs](https://www.engineering.com/?p=17283)
