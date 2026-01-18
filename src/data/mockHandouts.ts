import { Handout } from '@/types';

export const mockHandouts: Record<string, Handout> = {
  'total-knee-replacement': {
    id: 'mock-tkr-001',
    procedure: 'Total Knee Replacement',
    procedureCode: '27447',
    generatedAt: new Date().toISOString(),
    title: 'After Your Total Knee Replacement: Recovery Guide',
    sections: [
      {
        id: 'overview',
        type: 'overview',
        title: 'Overview',
        content: `<p>You have just undergone <strong>total knee replacement surgery</strong> (also called total knee arthroplasty). This procedure replaces your damaged knee joint with an artificial implant made of metal and plastic components.<sup>1</sup></p>
<p>Most patients spend <strong>1-3 days</strong> in the hospital after surgery. Your recovery will take several months, but most people return to normal daily activities within <strong>6-12 weeks</strong>.<sup>2</sup></p>
<p>This guide will help you understand what to expect and how to care for yourself at home.</p>`,
        citationIds: [1, 2],
      },
      {
        id: 'pain-management',
        type: 'pain-management',
        title: 'Pain Management',
        content: `<p>Some pain and discomfort after surgery is normal and expected. Your pain should gradually improve each week.<sup>3</sup></p>
<h4>Medications</h4>
<ul>
<li>Take your prescribed pain medication as directed</li>
<li>You may use over-the-counter acetaminophen (Tylenol) between doses if approved by your surgeon</li>
<li><strong>Avoid NSAIDs</strong> (ibuprofen, naproxen) unless specifically approved, as they may affect bone healing<sup>4</sup></li>
</ul>
<h4>Ice Therapy</h4>
<ul>
<li>Apply ice packs to your knee for <strong>20 minutes at a time</strong></li>
<li>Use a thin towel between the ice and your skin</li>
<li>Ice is most effective in the first 2 weeks after surgery</li>
</ul>
<h4>Elevation</h4>
<ul>
<li>Keep your leg elevated above heart level when resting</li>
<li>This reduces swelling and pain</li>
</ul>`,
        citationIds: [3, 4],
      },
      {
        id: 'activity-restrictions',
        type: 'activity-restrictions',
        title: 'Activity Restrictions',
        content: `<h4>First 2 Weeks</h4>
<ul>
<li>Use your walker or crutches for all walking</li>
<li>Do not bear full weight unless cleared by your surgeon</li>
<li>Avoid stairs if possible; if necessary, lead with your good leg going up, surgical leg going down<sup>5</sup></li>
</ul>
<h4>Weeks 2-6</h4>
<ul>
<li>Transition to a cane as directed by your physical therapist</li>
<li>Begin gentle strengthening exercises</li>
<li>Short walks (5-10 minutes) several times daily</li>
</ul>
<h4>Avoid These Activities for 12 Weeks</h4>
<ul>
<li>Running or jogging</li>
<li>High-impact sports</li>
<li>Deep squatting or kneeling</li>
<li>Twisting movements on your surgical leg</li>
</ul>`,
        citationIds: [5],
      },
      {
        id: 'wound-care',
        type: 'wound-care',
        title: 'Wound Care',
        content: `<h4>Incision Care</h4>
<ul>
<li>Keep your incision <strong>clean and dry</strong></li>
<li>Do not submerge in water (no baths, pools, hot tubs) until fully healed</li>
<li>Showering is typically allowed 48-72 hours after surgery with waterproof covering</li>
</ul>
<h4>Dressing Changes</h4>
<ul>
<li>Change dressings as instructed by your surgical team</li>
<li>Watch for signs of infection: increasing redness, warmth, drainage, or fever</li>
</ul>
<h4>Staples/Sutures</h4>
<ul>
<li>Will be removed at your follow-up appointment (typically 10-14 days)</li>
</ul>`,
        citationIds: [],
      },
      {
        id: 'warning-signs',
        type: 'warning-signs',
        title: 'Warning Signs - When to Call Your Doctor',
        content: `<p><strong>Call your surgeon immediately if you experience:</strong></p>
<ul>
<li>Fever over <strong>101.5°F (38.6°C)</strong></li>
<li>Increasing pain not relieved by medication</li>
<li>Significant swelling, redness, or warmth around the incision</li>
<li>Drainage or opening of the incision</li>
<li>Calf pain, swelling, or tenderness (possible blood clot)<sup>6</sup></li>
<li><strong>Chest pain or difficulty breathing</strong> (seek emergency care)</li>
</ul>
<h4>Signs of Blood Clot (Deep Vein Thrombosis)</h4>
<ul>
<li>Pain or tenderness in your calf or thigh</li>
<li>Swelling in your leg</li>
<li>Warmth or redness in your leg</li>
</ul>
<p>If you suspect a blood clot, contact your doctor immediately or go to the emergency room.</p>`,
        citationIds: [6],
      },
      {
        id: 'follow-up-care',
        type: 'follow-up-care',
        title: 'Follow-Up Care',
        content: `<h4>Scheduled Appointments</h4>
<ul>
<li><strong>10-14 days:</strong> Wound check and staple/suture removal</li>
<li><strong>6 weeks:</strong> X-rays and progress evaluation</li>
<li><strong>3 months:</strong> Final post-operative assessment</li>
</ul>
<h4>Physical Therapy</h4>
<ul>
<li>Begin as directed (usually within 1-2 days of surgery)</li>
<li>Attend all scheduled sessions</li>
<li>Perform home exercises daily as prescribed<sup>7</sup></li>
</ul>
<h4>Long-Term</h4>
<ul>
<li>Your new knee can last <strong>15-20 years or more</strong> with proper care</li>
<li>Avoid high-impact activities to protect your implant</li>
<li>Inform all healthcare providers about your knee replacement before any procedures</li>
</ul>`,
        citationIds: [7],
      },
    ],
    citations: [
      {
        id: 1,
        authors: 'Smith JA, Johnson MB',
        title: 'Outcomes in total knee arthroplasty: A comprehensive review',
        journal: 'J Bone Joint Surg Am',
        year: 2023,
        volume: '105(3)',
        pages: '234-241',
        doi: '10.2106/JBJS.22.01234',
      },
      {
        id: 2,
        authors: 'Chen R, Williams K',
        title: 'Recovery timelines after total knee arthroplasty: Patient expectations vs reality',
        journal: 'Orthopedics',
        year: 2022,
        volume: '45(2)',
        pages: '112-118',
      },
      {
        id: 3,
        authors: 'Patel S, Anderson M, Lee J',
        title: 'Multimodal pain management following knee replacement surgery',
        journal: 'Pain Medicine',
        year: 2023,
        volume: '24(4)',
        pages: '445-452',
      },
      {
        id: 4,
        authors: 'Brown T, Davis R',
        title: 'Effects of NSAIDs on bone healing after orthopedic surgery: A systematic review',
        journal: 'J Orthop Res',
        year: 2021,
        volume: '39(1)',
        pages: '78-85',
      },
      {
        id: 5,
        authors: 'American Academy of Orthopaedic Surgeons',
        title: 'Clinical practice guideline: Post-operative activity following total knee arthroplasty',
        journal: 'AAOS Clinical Practice Guidelines',
        year: 2022,
      },
      {
        id: 6,
        authors: 'Thompson M, Garcia L, Kim S',
        title: 'Venous thromboembolism prevention and detection after total knee arthroplasty',
        journal: 'Thromb Res',
        year: 2023,
        volume: '221',
        pages: '15-22',
      },
      {
        id: 7,
        authors: 'Wilson A, Moore B',
        title: 'Evidence-based physical therapy protocols following total knee arthroplasty',
        journal: 'Phys Ther',
        year: 2022,
        volume: '102(5)',
        pages: 'pzac034',
      },
    ],
    qualityMetrics: {
      overallScore: 87,
      readabilityGrade: 7.2,
      citationCoverage: 85,
      completeness: 100,
      safetyCheck: 'passed',
    },
  },

  'cesarean-section': {
    id: 'mock-csection-001',
    procedure: 'Cesarean Section (C-Section)',
    procedureCode: '59510',
    generatedAt: new Date().toISOString(),
    title: 'After Your Cesarean Section: Recovery Guide',
    sections: [
      {
        id: 'overview',
        type: 'overview',
        title: 'Overview',
        content: `<p>You have just delivered your baby via <strong>cesarean section</strong> (C-section), a surgical procedure to deliver your baby through an incision in your abdomen and uterus.<sup>1</sup></p>
<p>Recovery from a C-section typically takes <strong>6-8 weeks</strong>, though you will feel progressively better each day. Most mothers stay in the hospital for <strong>2-4 days</strong> after delivery.<sup>2</sup></p>
<p>This guide will help you care for yourself while also caring for your new baby.</p>`,
        citationIds: [1, 2],
      },
      {
        id: 'pain-management',
        type: 'pain-management',
        title: 'Pain Management',
        content: `<p>It is normal to experience pain and discomfort around your incision for several weeks.<sup>3</sup></p>
<h4>Medications</h4>
<ul>
<li>Take prescribed pain medication as directed</li>
<li>Most pain medications are safe while breastfeeding - ask your doctor if you have concerns</li>
<li>Ibuprofen (Motrin, Advil) is typically safe and helps with inflammation<sup>4</sup></li>
</ul>
<h4>Comfort Measures</h4>
<ul>
<li>Use a pillow to support your abdomen when coughing, laughing, or breastfeeding</li>
<li>Apply a heating pad on low setting to your back for muscle pain</li>
<li>Take slow, deep breaths to prevent lung complications</li>
</ul>`,
        citationIds: [3, 4],
      },
      {
        id: 'activity-restrictions',
        type: 'activity-restrictions',
        title: 'Activity Restrictions',
        content: `<h4>First 2 Weeks</h4>
<ul>
<li>Rest as much as possible - sleep when baby sleeps</li>
<li>Avoid lifting anything heavier than your baby</li>
<li>Take short, slow walks to promote healing and prevent blood clots<sup>5</sup></li>
<li>Do not drive while taking narcotic pain medication</li>
</ul>
<h4>Weeks 2-6</h4>
<ul>
<li>Gradually increase activity as tolerated</li>
<li>Continue to avoid heavy lifting (nothing over 10-15 lbs)</li>
<li>Climbing stairs is okay, but take it slowly</li>
</ul>
<h4>Wait Until Cleared by Your Doctor</h4>
<ul>
<li><strong>Sexual intercourse:</strong> Typically 6 weeks</li>
<li><strong>Exercise:</strong> Light exercise at 6 weeks, strenuous at 8-12 weeks</li>
<li><strong>Swimming/baths:</strong> After incision is fully healed (usually 3-4 weeks)</li>
</ul>`,
        citationIds: [5],
      },
      {
        id: 'wound-care',
        type: 'wound-care',
        title: 'Wound Care',
        content: `<h4>Incision Care</h4>
<ul>
<li>Keep the incision <strong>clean and dry</strong></li>
<li>Gently wash with soap and water during showers</li>
<li>Pat dry thoroughly - do not rub</li>
<li>Wear loose, comfortable clothing that does not rub on the incision</li>
</ul>
<h4>What to Expect</h4>
<ul>
<li>Mild redness and swelling around the incision is normal</li>
<li>Numbness or tingling around the scar may last several months</li>
<li>The scar will fade over time but will remain visible</li>
</ul>
<h4>Stitches/Staples</h4>
<ul>
<li>Dissolvable stitches will disappear on their own</li>
<li>Staples or non-dissolvable stitches are removed at your follow-up (7-10 days)</li>
</ul>`,
        citationIds: [],
      },
      {
        id: 'warning-signs',
        type: 'warning-signs',
        title: 'Warning Signs - When to Call Your Doctor',
        content: `<p><strong>Call your doctor immediately if you experience:</strong></p>
<ul>
<li>Fever over <strong>100.4°F (38°C)</strong></li>
<li>Increasing pain or redness at your incision</li>
<li>Incision opening or draining pus</li>
<li>Heavy vaginal bleeding (soaking more than one pad per hour)<sup>6</sup></li>
<li>Foul-smelling vaginal discharge</li>
<li>Pain or burning with urination</li>
<li>Leg pain or swelling (possible blood clot)</li>
</ul>
<h4>Seek Emergency Care For</h4>
<ul>
<li>Chest pain or difficulty breathing</li>
<li>Severe headache or vision changes</li>
<li>Thoughts of harming yourself or your baby<sup>7</sup></li>
</ul>`,
        citationIds: [6, 7],
      },
      {
        id: 'follow-up-care',
        type: 'follow-up-care',
        title: 'Follow-Up Care',
        content: `<h4>Scheduled Appointments</h4>
<ul>
<li><strong>1-2 weeks:</strong> Incision check (if staples need removal)</li>
<li><strong>6 weeks:</strong> Complete postpartum examination</li>
</ul>
<h4>Breastfeeding Support</h4>
<ul>
<li>C-section does not affect your ability to breastfeed<sup>8</sup></li>
<li>Use pillows to support baby and protect your incision</li>
<li>Contact a lactation consultant if you have difficulties</li>
</ul>
<h4>Emotional Health</h4>
<ul>
<li>Baby blues (mood swings, crying) are common in the first 2 weeks</li>
<li>If feelings of sadness persist beyond 2 weeks, contact your doctor</li>
<li>Postpartum depression is treatable - do not hesitate to ask for help</li>
</ul>`,
        citationIds: [8],
      },
    ],
    citations: [
      {
        id: 1,
        authors: 'American College of Obstetricians and Gynecologists',
        title: 'ACOG Practice Bulletin: Cesarean Delivery',
        journal: 'Obstet Gynecol',
        year: 2021,
        volume: '137(3)',
        pages: 'e71-e87',
      },
      {
        id: 2,
        authors: 'Martin JA, Hamilton BE, Osterman MJ',
        title: 'Births: Final Data for 2022',
        journal: 'Natl Vital Stat Rep',
        year: 2023,
        volume: '72(1)',
        pages: '1-50',
      },
      {
        id: 3,
        authors: 'Kerai S, Saxena KN, Taneja B',
        title: 'Post-cesarean analgesia: Current perspectives',
        journal: 'Int J Womens Health',
        year: 2022,
        volume: '14',
        pages: '467-476',
      },
      {
        id: 4,
        authors: 'Berens P, Labbok M',
        title: 'ABM Clinical Protocol: Analgesia and anesthesia for the breastfeeding mother',
        journal: 'Breastfeed Med',
        year: 2022,
        volume: '17(5)',
        pages: '403-411',
      },
      {
        id: 5,
        authors: 'Mackeen AD, Packard RE, Ota E',
        title: 'Antibiotic regimens for postpartum endometritis',
        journal: 'Cochrane Database Syst Rev',
        year: 2021,
        volume: '2',
        pages: 'CD001067',
      },
      {
        id: 6,
        authors: 'Committee on Practice Bulletins',
        title: 'ACOG Practice Bulletin: Postpartum Hemorrhage',
        journal: 'Obstet Gynecol',
        year: 2023,
        volume: '141(4)',
        pages: 'e112-e133',
      },
      {
        id: 7,
        authors: 'American Psychiatric Association',
        title: 'Practice guideline for the treatment of patients with major depressive disorder',
        journal: 'Am J Psychiatry',
        year: 2022,
        volume: '179(suppl)',
        pages: '1-38',
      },
      {
        id: 8,
        authors: 'Prior E, Santhakumaran S, Gale C',
        title: 'Breastfeeding after cesarean delivery: A systematic review and meta-analysis',
        journal: 'Am J Clin Nutr',
        year: 2022,
        volume: '116(2)',
        pages: '512-521',
      },
    ],
    qualityMetrics: {
      overallScore: 91,
      readabilityGrade: 6.8,
      citationCoverage: 88,
      completeness: 100,
      safetyCheck: 'passed',
    },
  },

  'laparoscopic-cholecystectomy': {
    id: 'mock-chole-001',
    procedure: 'Laparoscopic Cholecystectomy',
    procedureCode: '47562',
    generatedAt: new Date().toISOString(),
    title: 'After Your Gallbladder Surgery: Recovery Guide',
    sections: [
      {
        id: 'overview',
        type: 'overview',
        title: 'Overview',
        content: `<p>You have just undergone <strong>laparoscopic cholecystectomy</strong>, a minimally invasive surgery to remove your gallbladder. This procedure is performed through several small incisions using a camera and specialized instruments.<sup>1</sup></p>
<p>Most patients go home the <strong>same day</strong> or within 24 hours of surgery. Full recovery typically takes <strong>1-2 weeks</strong>, though you may feel better within a few days.<sup>2</sup></p>
<p>Your body can digest food normally without a gallbladder, though some dietary adjustments may be needed initially.</p>`,
        citationIds: [1, 2],
      },
      {
        id: 'pain-management',
        type: 'pain-management',
        title: 'Pain Management',
        content: `<p>You may experience several types of discomfort after surgery:<sup>3</sup></p>
<h4>Incision Pain</h4>
<ul>
<li>Mild to moderate pain at the incision sites is normal</li>
<li>Take prescribed pain medication as directed</li>
<li>Over-the-counter acetaminophen or ibuprofen may be sufficient after 1-2 days</li>
</ul>
<h4>Shoulder Pain</h4>
<ul>
<li>Shoulder pain from gas used during surgery is common</li>
<li>This typically resolves within <strong>24-48 hours</strong></li>
<li>Walking and gentle movement helps release trapped gas<sup>4</sup></li>
</ul>
<h4>Abdominal Bloating</h4>
<ul>
<li>Some bloating is normal for several days</li>
<li>Avoid carbonated beverages</li>
<li>Eat small, frequent meals</li>
</ul>`,
        citationIds: [3, 4],
      },
      {
        id: 'activity-restrictions',
        type: 'activity-restrictions',
        title: 'Activity Restrictions',
        content: `<h4>First Week</h4>
<ul>
<li>Rest when tired, but take short walks several times daily</li>
<li>No lifting over <strong>10 pounds</strong> (about a gallon of milk)</li>
<li>No driving while taking prescription pain medication</li>
<li>You may climb stairs carefully</li>
</ul>
<h4>Weeks 1-2</h4>
<ul>
<li>Gradually increase activity as tolerated</li>
<li>Most people return to desk jobs within <strong>1 week</strong><sup>5</sup></li>
<li>Physical labor may require 2-4 weeks off work</li>
</ul>
<h4>After 2 Weeks</h4>
<ul>
<li>Resume normal activities including exercise</li>
<li>Listen to your body - if something causes pain, stop</li>
</ul>`,
        citationIds: [5],
      },
      {
        id: 'wound-care',
        type: 'wound-care',
        title: 'Wound Care',
        content: `<h4>Incision Care</h4>
<ul>
<li>You will have <strong>3-4 small incisions</strong> on your abdomen</li>
<li>Keep incisions clean and dry for 48 hours</li>
<li>After 48 hours, you may shower - gently wash with soap and water</li>
<li>Do not soak in baths, pools, or hot tubs for 2 weeks</li>
</ul>
<h4>Bandages</h4>
<ul>
<li>Small adhesive strips (Steri-Strips) may cover your incisions</li>
<li>Let these fall off naturally (usually within 1-2 weeks)</li>
<li>If bandages get wet, pat dry or replace</li>
</ul>
<h4>What to Expect</h4>
<ul>
<li>Mild bruising around incisions is normal</li>
<li>Incisions may feel itchy as they heal</li>
</ul>`,
        citationIds: [],
      },
      {
        id: 'warning-signs',
        type: 'warning-signs',
        title: 'Warning Signs - When to Call Your Doctor',
        content: `<p><strong>Call your doctor if you experience:</strong></p>
<ul>
<li>Fever over <strong>101°F (38.3°C)</strong></li>
<li>Increasing abdominal pain not relieved by medication</li>
<li>Redness, swelling, or drainage from incisions</li>
<li>Nausea or vomiting lasting more than 24 hours<sup>6</sup></li>
<li>Yellowing of skin or eyes (jaundice)</li>
<li>No bowel movement for more than 3 days</li>
</ul>
<h4>Seek Emergency Care For</h4>
<ul>
<li>Severe abdominal pain</li>
<li>Chest pain or difficulty breathing</li>
<li>Signs of infection (fever, chills, spreading redness)</li>
</ul>`,
        citationIds: [6],
      },
      {
        id: 'follow-up-care',
        type: 'follow-up-care',
        title: 'Follow-Up Care',
        content: `<h4>Appointments</h4>
<ul>
<li><strong>1-2 weeks:</strong> Post-operative check-up with your surgeon</li>
<li>Call sooner if you have any concerns</li>
</ul>
<h4>Diet After Surgery</h4>
<ul>
<li>Start with <strong>clear liquids</strong>, then advance to regular diet as tolerated</li>
<li>Some people experience loose stools or diarrhea initially<sup>7</sup></li>
<li>Avoid fatty, greasy, or fried foods for 2-4 weeks</li>
<li>Gradually reintroduce foods and note any that cause discomfort</li>
</ul>
<h4>Long-Term</h4>
<ul>
<li>Most people can eat normally after recovery</li>
<li>About <strong>10-20%</strong> of patients may have ongoing digestive changes<sup>8</sup></li>
<li>Contact your doctor if digestive issues persist</li>
</ul>`,
        citationIds: [7, 8],
      },
    ],
    citations: [
      {
        id: 1,
        authors: 'Society of American Gastrointestinal and Endoscopic Surgeons',
        title: 'Guidelines for the clinical application of laparoscopic biliary tract surgery',
        journal: 'Surg Endosc',
        year: 2022,
        volume: '36',
        pages: '1-12',
      },
      {
        id: 2,
        authors: 'Keus F, de Jong JA, Gooszen HG',
        title: 'Laparoscopic versus open cholecystectomy for patients with symptomatic cholecystolithiasis',
        journal: 'Cochrane Database Syst Rev',
        year: 2021,
        volume: '3',
        pages: 'CD006231',
      },
      {
        id: 3,
        authors: 'Gurusamy KS, Vaughan J, Toon CD',
        title: 'Pharmacological interventions for prevention or treatment of postoperative pain after laparoscopic cholecystectomy',
        journal: 'Cochrane Database Syst Rev',
        year: 2022,
        volume: '5',
        pages: 'CD008261',
      },
      {
        id: 4,
        authors: 'Donatsky AM, Bjerrum F, Gögenür I',
        title: 'Surgical techniques to minimize shoulder pain after laparoscopic cholecystectomy',
        journal: 'Surg Endosc',
        year: 2023,
        volume: '37',
        pages: '234-242',
      },
      {
        id: 5,
        authors: 'Barkun JS, Barkun AN, Sampalis JS',
        title: 'Return to work and quality of life after laparoscopic cholecystectomy',
        journal: 'Ann Surg',
        year: 2021,
        volume: '273',
        pages: '45-52',
      },
      {
        id: 6,
        authors: 'Vollmer CM, Callery MP',
        title: 'Biliary injury following laparoscopic cholecystectomy: Why still a problem?',
        journal: 'Gastroenterology',
        year: 2022,
        volume: '162(1)',
        pages: '12-15',
      },
      {
        id: 7,
        authors: 'Fisher M, Spilias DC, Tong LK',
        title: 'Diarrhoea after laparoscopic cholecystectomy: Incidence and main determinants',
        journal: 'ANZ J Surg',
        year: 2022,
        volume: '92',
        pages: '1178-1183',
      },
      {
        id: 8,
        authors: 'Latenstein CSS, Wennmacker SZ, de Jong JJ',
        title: 'Etiologies of long-term postcholecystectomy symptoms',
        journal: 'Gastroenterology Res Pract',
        year: 2023,
        volume: '2023',
        pages: '8674982',
      },
    ],
    qualityMetrics: {
      overallScore: 89,
      readabilityGrade: 7.0,
      citationCoverage: 82,
      completeness: 100,
      safetyCheck: 'passed',
    },
  },
};

// Get handout by procedure ID
export const getHandoutByProcedureId = (procedureId: string): Handout | undefined => {
  return mockHandouts[procedureId];
};

// Check if handout exists for procedure
export const hasHandoutForProcedure = (procedureId: string): boolean => {
  return procedureId in mockHandouts;
};

// Get all available procedure IDs with handouts
export const getAvailableHandoutProcedureIds = (): string[] => {
  return Object.keys(mockHandouts);
};
