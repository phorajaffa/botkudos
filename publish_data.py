#!/usr/bin/env python3
"""Story data for the bulk publish of 99 approved botkudos stories.
Run: python3 publish_data.py  -> writes stories_draft.json (summaries filled by subagents)."""
import json

# (num, title, source_name, pub_date, category, kudos_level, url_key, notes)
STORIES = [
# Batch 1
(1, "Nanorobots That Swim Through Your Body to Deliver Medicine Are Coming. On.", "IEEE Spectrum", "2017", "Robots", 2, "medical-microbots-take-a-fantastic", "Nano-scale robots that move freely in the body, communicate, do jobs, then degrade."),
(3, "A Robotic Teddy Bear Is Making Hospitalized Kids Feel Better. On.", "MIT Media Lab", "2019", "Robots", 2, "huggable", "MIT's Huggable improved emotional and physical outcomes for 50+ hospitalized kids in a Pediatrics study."),
(4, "This Man Controls a Robotic Arm With His Thoughts. On.", "Bloomberg", "2015", "Robots", 2, "thought-controlled-robotic-arm", "Osseointegrated prosthetic arm wired directly to the skeleton."),
(5, "Alphabet's Wing Drones Hit 100,000 Deliveries. On.", "The Verge", "2021", "Robots", 1, "drone-delivery-google-alphabet-wing-milestone", "Slowly, then suddenly."),
(6, "ISRO Launched 20 Satellites on a Single Rocket. On.", "The Hindu", "2016", "Science", 2, "isros-20in1", "20 satellites, about 26 minutes."),
(7, "SpaceX Took the Commercial Launch Crown From Russia. On.", "Ars Technica", "2018", "Science", 2, "surrendered-to-spacex", "How SpaceX seized the global launch market."),
(8, "A Teenager Built an AI That Diagnoses Her Grandfather's Eye Disease. On.", "IEEE Spectrum", "2018", "Medicine", 2, "teenage-whiz-kid", "A smartphone, a 3D-printed lens, an AI system, and Kavya Kopparapu."),
(9, "An AI Recreated a Nobel-Winning Physics Experiment in One Hour. On.", "ScienceDaily", "2016-05", "Science", 1, "nobel-winning-experiment-recreated-by-ai", "ANU's Bose-Einstein condensate, learned from scratch."),
(10, "A Soft Exosuit Is Helping Stroke Victims Walk Again. On.", "The Guardian", "2016", "Robots", 1, "robot-exosuit-harvard", "Low-cost, low-tech Harvard exosuit."),
(11, "Gene Editing Might Cure HIV. The First Trial Results Are In. On.", "The Conversation", "2023", "Medicine", 2, "can-hiv-be-cured-using-gene-editing", "A startup's CRISPR approach, first results 2024."),
# Batch 2
(12, "Overnight Success Takes Decades: The mRNA Story. On.", "Nature", "2021", "Science", 2, "s41578-021-00358-0", "The decades of slogging behind the overnight mRNA miracle."),
(13, "The Painting Robot That Didn't Steal Anyone's Job. On.", "Wired", "2016", "Robots", 1, "the-tale-of-the-painting-robot", "Robots that transformed the workforce instead of replacing it."),
(15, "An AI App Is Reading Chest X-Rays for TB in Rural India. On.", "The New York Times", "2020-11", "Medicine", 2, "tuberculosis-ai-apps", "Qure.ai augmenting healthcare capacity where doctors are scarce."),
(16, "AI Can Hear a Heart Attack in Your 911 Call. On.", "MIT Technology Review", "2018", "Medicine", 2, "ai-could-diagnose-your-heart-attack", "Diagnosing cardiac arrest from a caller's voice, better than human dispatchers."),
(18, "Translation Apps Are Quietly Making the World Closer. On.", "The New York Times", "2015", "Accessibility", 1, "language-translation-tech", "The internet made the world smaller; translation will make it closer."),
(19, "Satellites Are Measuring Economies in Real Time. On.", "Bloomberg", "2015", "Science", 1, "satellite-images-show-economies", "Cheap cameras and big data rewriting economic measurement."),
# Batch 3
(21, "AI and Automation Are Collapsing the Drug Discovery Timeline. On.", "MIT Technology Review", "2023", "Science", 2, "ai-automation-drug-development", "Finding the right drug for the right patient, faster."),
(22, "Gene Therapies for Rare Diseases Are Here. On.", "Bloomberg", "2019", "Medicine", 2, "one-shot-drug-for-sicily", "One-shot cures arriving; now the fight is price."),
(23, "The Battery Made of Rust That Stores Power for 100 Hours. On.", "TechXplore", "2021", "Climate", 2, "iron-air", "Form Energy's iron-air battery at a tenth of lithium's cost."),
(24, "A 20-Year-Old Invented a Life-Saving Smart Wheelchair. On.", "BBC", "2014", "Accessibility", 1, "news/world-29484922", ""),
(25, "Paralyzed With a Severed Spinal Cord, He Walks Again. On.", "BBC", "2022", "Medicine", 3, "science-environment-60258620", "An implant bridges the injury."),
(26, "A Brain Chip Gave a Paralyzed Man His Hand Back. On.", "The New York Times", "2016", "Medicine", 2, "paralysis-limb-reanimation-brain-chip", ""),
(27, "A Brain Implant Turned a Paralyzed Man's Thoughts Into Words. On.", "NPR", "2021", "Medicine", 2, "experimental-brain-implant", ""),
(28, "A New Drug Delays Type 1 Diabetes in Kids. On.", "The New York Times", "2022", "Medicine", 2, "fda-type-1-diabetes-delay", "A full, normal childhood, postponed disease."),
(29, "The World's Best Hope for Enough Covid Vaccine. On.", "Bloomberg", "2020", "Medicine", 2, "2020-covid-vaccine-serum-india", "Serum Institute's manufacturing scale-up."),
# Batch 4
(30, '"For Us, This Technology Is a Game-Changer": Europe\'s Emergency Workers Turn to Drones. On.', "The New York Times", "2016", "Robots", 2, "europe-emergency-drones", ""),
(31, "Gene Therapy Made Deaf Mice Hear Again. On.", "Scientific American", "2017", "Medicine", 2, "gene-therapy-mice-hearing-loss", "Virus ferries healthy genes into inner ears."),
(32, "A Bold Effort to Cure HIV Using CRISPR. On.", "Wired", "2019", "Medicine", 2, "a-bold-effort-to-cure-hiv-using-crispr", ""),
(33, "The Hubble Is Falling. SpaceX Might Give It a Lift. On.", "The New York Times", "2022", "Science", 1, "nasa-hubble-spacex-polaris", "A billionaire and SpaceX explore a reboost mission."),
(34, "Sesame Phone: A Hands-Free Smartphone for Paralyzed Users. On.", "Bloomberg", "2016", "Accessibility", 1, "sesame-phone-a-hands-free", ""),
(35, "Ford's Driverless Cars Passed the Snow Test. On.", "BBC", "2016", "Robots", 1, "bbc.com/news/technology-35280632", ""),
(36, "Transplant Surgery Got a Paralyzed Man Walking Again. On.", "BBC", "2014", "Medicine", 2, "health-29645760", '"This is just fantastic."'),
(37, "The $70,000 Exoskeleton That Helps the Paralyzed Walk. On.", "The Japan Times", "2015", "Robots", 2, "exoskeleton-helps-paralyzed-walk-faces-bur", "Already approved in the US and EU."),
(38, "Hi-Tech Agriculture Is Freeing the Farmer From His Fields. On.", "The Guardian", "2015", "Science", 1, "hi-tech-agriculture-is-freeing-farmer", "Satellite steering, drones, sensor fields."),
(39, "The Robot Surgeon That Stitches Better Than Humans. On.", "Johns Hopkins University", "2016", "Robots", 2, "nimble-fingered-robot-outperforms", "STAR's submillimeter sutures beat its own inventors."),
(40, "CRISPR Offers Hope for Muscular Dystrophy. On.", "The New York Times", "2016", "Medicine", 2, "gene-therapy-muscular-dystrophy", ""),
(41, "Why Gene Editing Has Scientists So Excited. On.", "The Wall Street Journal", "2015", "Science", 2, "why-gene-editing-technology-has-scientists-excited", '"Go right to the root cause of that disease and repair the broken gene."'),
(42, "An mRNA Vaccine Fully Immunized Mice Against Malaria. On.", "MedicalXpress", "2021", "Medicine", 2, "mrna-vaccine-yields-full-malaria", ""),
(43, "Controlling Google Glass With Brainwaves. On.", "BBC", "2014", "Accessibility", 1, "technology-28237582", '"Can do wonders for people with limited abilities."'),
(44, "The Malaria Vaccine That Beat Expectations at 77% Efficacy. On.", "MedicalXpress", "2021", "Medicine", 3, "malaria-vaccine-who-specified-efficacy-goal", "First to hit WHO's 75% goal; $2 a dose."),
(45, "The Armada of Saildrones Mapping the Oceans. On.", "Bloomberg", "2018", "Science", 1, "this-man-is-building-an-armada-of-saildrones", "Autonomous sailing drones collecting research data."),
(46, "ISRO Launched 104 Satellites on One Rocket. On.", "Nature", "2017", "Science", 3, "nindia.2017.35", "A world record on the famously frugal PSLV."),
(47, "The Robot With Its Head in the Cloud. On.", "MIT Technology Review", "2017", "Robots", 1, "a-robot-with-its-head-in-the-cloud", "Warehouse picker that shares what it learns with a hive mind."),
(48, "Old Phones and Smart Software Are Catching Illegal Loggers. On.", "The New York Times", "2019", "Climate", 2, "indonesia-logging-deforestation", "Chainsaw sounds trigger the alarm."),
(49, "The Nobel for the Brain's Inner GPS. On.", "Nobel Prize", "2014", "Science", 2, "nobelprize.org", "The discovery of place and grid cells."),
# Batch 5
(50, '"Scientists Make Telepathy Breakthrough." On.', "BBC", "2014", "Science", 1, "technology-29704953", "Brain-to-brain communication, demonstrated."),
(51, "A Robot Will Beam Live Moon Pictures to Your Headset. On.", "BBC", "2014", "Science", 1, "robot-will-beam-live-moon-pictures", ""),
(52, "The FDA Approved VR Movies as a Treatment for Lazy Eye. On.", "The Verge", "2021", "Medicine", 2, "fda-vr-tv-movies-treatment-lazy-eye", "Real therapy for kids' amblyopia."),
(53, "CRISPR's Next Act: Fighting Climate Change and Feeding the World. On.", "Wired", "2023", "Science", 2, "crispr-gene-editing-climate", "Doudna lab on what's next."),
(54, "Your Cough Has a Sound. AI Can Hear Disease in It. On.", "The Wall Street Journal", "2021", "Medicine", 2, "diagnose-respiratory-illness-smartphone", "Smartphone diagnosis of respiratory illness."),
(55, "How Robots Are Making Better Drugs, Faster. On.", "The Wall Street Journal", "2018", "Science", 2, "how-robots-are-improving-pharma-research", ""),
(56, "The Terminator-2 3D Printer: Solid Objects From Liquid in Minutes. On.", "Popular Science", "2015", "Science", 2, "terminator-2-inspired-3d-print", "CLIP grows parts 25-100x faster."),
(57, "Blue Origin Made Solar Cells From Moon Dust. On.", "New Atlas", "2023-07", "Science", 2, "building-solar-cells-on-the-moon", "Blue Alchemist turns regolith into power systems."),
(58, "Robots to Make Robots at ABB's $150M Factory. On.", "EE News Europe", "2018", "Robots", 1, "robots-to-make-robots-at-abbs-new", ""),
(59, "Stem Cells Reversed Type 1 Diabetes in a Woman. On.", "Nature", "2024", "Medicine", 3, "d41586-024-03129-3", "Reprogrammed transplant, reported in Nature."),
(60, "The Ingenious Way Iranians Beam Banned Data Over Satellite TV. On.", "Wired", "2016", "Accessibility", 1, "ingenious-way-iranians-using-satellite-tv", ""),
(61, "Weavers Turn Silk Into Diabetes Test Strips at a Third of the Cost. On.", "NPR", "2015", "Medicine", 2, "weavers-turn-silk-into-diabetes-test", ""),
(62, "The App That Diagnoses Genetic Disorders at a Glance. On.", "Wired", "2017", "Medicine", 2, "computers-can-tell-glance-youve-got-genetic", "What took doctors 16 years took it minutes."),
(63, "A Robot That Helps Autistic Pupils Build Social Skills. On.", "BBC", "2014", "Robots", 2, "technology-30053748", "Robots complementing human support."),
(64, "The Hand of a Superhero: 3D-Printed Prosthetics Kids Actually Want. On.", "The New York Times", "2015", "Accessibility", 2, "hand-of-a-superhero", "Cheap prosthetics that don't suggest disability."),
(65, "Stem Cell Surgery Regrew Eye Lenses in 12 Children. On.", "ScienceDaily", "2016", "Medicine", 3, "remarkable-surgery-uses-stem-cells", "Cataract infants regrew functional lenses."),
(66, "A Paralyzed Man Walked Again on Brain Power Alone. On.", "UC Irvine", "2015", "Medicine", 3, "a-man-walked-again-using-brain-machine-interface", "UCI's EEG system bypassed his spinal cord."),
(67, "The Rowbot: A Roomba for the Cornfield. On.", "KNKX", "2013", "Robots", 1, "a-nimble-wheeled-farm-robot", "Tiny robot fertilizes plant by plant, cutting runoff."),
(68, "The Drone That Maps, Finds, and Detonates Landmines. On.", "World Economic Forum", "2016", "Robots", 3, "landmine-hunting-drone", "20x faster, 200x cheaper; a landmine-free world in a decade."),
# Batch 6
(70, 'Asked Via a Mind-Reading Device, Locked-In Patients Said "I Love to Live." On.', "Inverse", "2017", "Medicine", 3, "mind-reading-paralyzed-want-to-live", "Three of four ALS patients answered yes."),
(71, "Drones Flew Blood to a Remote Hospital in 18 Minutes. On.", "News18", "2021", "Medicine", 2, "drone-used-to-transport-blood-from-remote-heal", "Uttarakhand's infrastructure leapfrog."),
(72, "World Energy Hit a Turning Point: Solar Cheaper Than Wind. On.", "Bloomberg", "2016", "Climate", 2, "world-energy-hits-a-turning-point-solar-that", ""),
(73, "The Diabetes Patients Hacking Together Their Own Bionic Pancreas. On.", "Wired", "2014", "Medicine", 2, "diabetes-patients-hacking-together-diy-bionic-pancreases", ""),
(74, "A Joystick-Controlled Robot That Peels a Membrane 1/100th of a mm Thick. On.", "BBC", "2016", "Robots", 2, "health-37246995", ""),
(75, "The Stem-Cell Bio-Ink for 3D Printing Living Tissue. On.", "Phys.org", "2016", "Medicine", 2, "bio-ink-d-stem-cells", ""),
(76, "The CAD Program for Designing Organisms From Scratch. On.", "IEEE Spectrum", "2021", "Science", 2, "with-this-cad-for-genomes", "GP-write's genome CAD."),
(77, "Rwanda Began Commercial Drone Deliveries of Blood. On.", "BBC", "2016", "Medicine", 2, "technology-37646474", '"Toys for some, life-savers for others."'),
(78, "Verily's AI Is Diagnosing Diabetic Blindness in Rural India. On.", "The New York Times", "2019", "Medicine", 2, "artificial-intelligence-eye-hospital-india", "Up and running in South India."),
(79, "Tega: The Squishy Robot Teaching Preschoolers Spanish. On.", "IEEE Spectrum", "2016", "Robots", 2, "tega-mit-latest-friendly-squishable-social-robot", ""),
(80, "Singapore's Self-Driving Cars Can Be Hailed With a Smartphone. On.", "The Verge", "2016", "Robots", 1, "singapore-self-driving-car-nutonomy", ""),
(81, "How Robots, Drones, and New Disaster Tech Are Saving Lives. On.", "CNN", "2015", "Robots", 2, "robot-disaster-technology", ""),
(82, "Satellites Can Pinpoint Poverty Where Surveys Can't. On.", "The New York Times", "2016", "Science", 2, "satellite-images-can-pinpoint-poverty", ""),
(83, "The Visor That Diagnoses a Stroke in Half a Minute. On.", "MedicalXpress", "2018-03", "Medicine", 2, "portable-device-severe-seconds-percent", "92% accuracy vs. 40-89% for standard exams."),
(84, "The World's First Robot-Assisted Operation Inside the Human Eye. On.", "University of Oxford", "2016", "Robots", 3, "robotic-surgery", "Preceyes robot at the John Radcliffe Hospital."),
(85, "The $1,000 Braille Tablet Made of Microfluidic Bubbles. On.", "TechXplore", "2016-01", "Accessibility", 2, "michigan-team-braille-tablet-widen", "Full-page tactile graphics for the blind."),
(86, "China Approved the World's First Commercial Brain Implant for Paralysis. On.", "Dong-A Science", "2026", "Medicine", 3, "dongascience.com/en/news/76876", "Neuracle's NEO restores hand movement."),
(87, "Can Nuclear Fusion Put the Brakes on Climate Change? On.", "The New Yorker", "2021-10", "Science", 3, "can-nuclear-fusion-put-the-brakes", ""),
(88, "He Typed 90 Characters a Minute Using Only His Thoughts. On.", "Science News", "2021-05", "Medicine", 3, "brain-implants-translate-handwriting-text", "Stanford's handwriting-decoding implant."),
(89, "Europe Approved the First Artificial Heart for Sale. On.", "Bloomberg", "2020", "Medicine", 3, "france-s-carmat-soars-as-artificial-heart-ho", "Carmat's aerospace-born device."),
# Batch 7
(90, "You'll Love Your Robot More If You Assemble It Yourself. On.", "Digital Trends", "2016", "Robots", 1, "robot-customization", "The IKEA effect applies to robots: self-assembly breeds ownership."),
(91, "Robots and Healthcare: Early Days, Promising Signs. On.", "BBC", "2015", "Robots", 1, "health-34271927", ""),
(92, "The Cyborg Cockroach That Could Search Collapsed Buildings. On.", "New Scientist", "2015", "Robots", 2, "2018225-cyborg-cockroach", "Texas A&M wired a microcontroller into a roach's nervous system."),
(93, "The Living Lights That Could Cut Our Energy Use. On.", "BBC", "2022", "Climate", 2, "the-living-lights-that-could-reduce-energy-use", "Bioluminescence as city lighting."),
(94, "Exoskeleton Technology Could Redefine Disability. On.", "Scientific American", "2023", "Accessibility", 2, "exoskeleton-technology-could-redefine-disability", ""),
(95, "Peek: The Smartphone Eye-Exam Kit That Could End Avoidable Blindness. On.", "TED", "2014", "Medicine", 2, "how-a-ted-fellows-new-app-could-help-restore-sight-to-millions", "Peek Retina adapter."),
(96, "A Five-Year-Old Got a 3D-Printed Prosthetic Hand for £50. On.", "BBC", "2014", "Accessibility", 2, "uk-scotland-highlands-islands-29441115", ""),
(97, "A Swarm of 1,024 Robots Working With No Central Intelligence. On.", "The Wall Street Journal", "2014", "Robots", 2, "harvard-scientists-devise-robot-swarm", "Harvard's kilobots."),
(98, "UPS Got the FAA Nod for Widespread Drone Deliveries. On.", "The Wall Street Journal", "2019", "Robots", 2, "ups-gets-faa-nod-for-widespread-drone-deliveries", "Health packages first."),
(99, "The FDA Approved the First Blood Sugar Monitor Without Finger Pricks. On.", "STAT", "2017-09", "Medicine", 2, "blood-sugar-monitor-finger-pricks-diabetes", ""),
(100, "Batteryless Devices That Talk Over Wi-Fi Using Ambient Backscatter. On.", "HEXUS", "2013", "Science", 2, "batteryless-wireless-devices-powered-ambient-backscatter", "UW ambient backscatter."),
(101, "The Smartshoe That Gives Directions Through Vibrations. On.", "The Wall Street Journal", "2014", "Accessibility", 2, "indias-answer-to-google-glass-the-smartshoe", "Indian startup's shoe, built for the visually impaired."),
(102, "Digital-Age Donations: USB Sticks for North Korea. On.", "BBC", "2016", "Accessibility", 1, "technology-35531228", ""),
(103, "Training Robots to Paint, Build, and Play. On.", "Forbes India", "2014", "Robots", 1, "how-to-train-your-robot", ""),
(104, 'The Material That "Learns" Like a Sea Slug. On.', "ScienceDaily", "2021-09", "Science", 2, "210914100037", "Nickel oxide shows habituation and sensitization, pointing to brain-like AI hardware."),
]

LEVEL_NAMES = {1: "Nice", 2: "Bravo", 3: "Legend"}

def match_urls():
    master = json.load(open("/home/hatch/workspace/botkudos-mockup/master_candidates.json"))
    results = {}
    missing = []
    for num, title, src, pub, cat, lvl, key, notes in STORIES:
        hits = [h for h in master if key.lower() in h["url"].lower()]
        if len(hits) == 1:
            results[num] = hits[0]["url"]
        else:
            missing.append((num, key, len(hits)))
    # Manually resolved URLs (verified replacements / originals not in archive)
    manual = {
        3: "https://www.media.mit.edu/articles/study-social-robots-can-benefit-hospitalized-children/",
        9: "http://www.sciencedaily.com/releases/2016/05/160516091544.htm",
        18: "http://bits.blogs.nytimes.com/2015/01/11/language-translation-tech-starting-to-deliver-on-its-promise/",
        19: "http://www.bloomberg.com/news/features/2015-07-08/satellite-images-show-economies-growing-and-shrinking-in-real-time",
        23: "https://techxplore.com/news/2021-07-energy-iron-air-hour-storage-battery.html",
        42: "https://medicalxpress.com/news/2021-06-mrna-vaccine-yields-full-malaria.html",
        44: "https://medicalxpress.com/news/2022-09-malaria-booster-vaccine-who-specified-efficacy.html",
        46: "https://www.nature.com/articles/nindia.2017.35",
        49: "https://www.nobelprize.org/prizes/medicine/2014/summary/",
        51: "http://www.bbc.com/news/technology-29704953",
        57: "https://newatlas.com/space/blue-alchemist-moon-dust-solar-cells/",
        68: "https://www.weforum.org/stories/all/this-is-a-landmine-hunting-drone/",
        70: "https://www.inverse.com/article/26086-mind-reading-device-als-patients",
        76: "https://spectrum.ieee.org/amp/with-this-cad-for-genomes-you-can-design-new-organisms-2652904032",
        83: "https://medicalxpress.com/news/2018-03-portable-device-severe-seconds-percent.html",
        85: "https://techxplore.com/news/2016-01-michigan-team-braille-tablet-widen.html",
        86: "https://www.dongascience.com/en/news/76876",
        88: "https://www.sciencenews.org/article/brain-implants-translate-handwriting-text",
        90: "http://www.digitaltrends.com/cool-tech/robot-customization/",
        92: "https://www.newscientist.com/article/2018225-cyborg-cockroach-has-its-nerves-controlled-wirelessly/",
        94: "https://www.scientificamerican.com/article/exoskeleton-technology-could-redefine-disability/",
        95: "https://blog.ted.com/how-a-ted-fellows-new-app-could-help-restore-sight-to-millions/amp/",
        100: "https://hexus.net/tech/news/network/58857-batteryless-wireless-devices-powered-ambient-backscatter/",
        104: "http://sciencedaily.com/releases/2021/09/210914100037.htm",
    }
    for num, key, n in missing:
        if num in manual:
            results[num] = manual[num]
    still_missing = [(num, key) for num, key, n in missing if num not in manual]
    return results, still_missing

if __name__ == "__main__":
    urls, missing = match_urls()
    print(f"matched: {len(urls)}/{len(STORIES)}")
    for num, key, n in missing:
        print("MISSING", num, key, f"({n} hits)")
    json.dump({str(k): v for k, v in urls.items()},
              open("/home/hatch/workspace/botkudos-repo/url_map.json", "w"), indent=1)
