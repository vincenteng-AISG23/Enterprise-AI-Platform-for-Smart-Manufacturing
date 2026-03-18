const pptxgen = require('pptxgenjs');
const { imageSizingCrop, imageSizingContain, warnIfSlideHasOverlaps, warnIfSlideElementsOutOfBounds, safeOuterShadow } = require('/home/oai/skills/slides/pptxgenjs_helpers');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'OpenAI';
pptx.company = 'OpenAI';
pptx.subject = 'Predictive Maintenance for Smart Factory';
pptx.title = 'Predictive Maintenance for Smart Factory';
pptx.lang = 'en-US';
const theme = {
  bg: 'F7FAFC',
  ink: '102A43',
  muted: '52606D',
  teal: '0F766E',
  teal2: '14B8A6',
  blue: '2563EB',
  orange: 'F59E0B',
  line: 'D9E2EC',
  white: 'FFFFFF',
  dark: '0B1F2A',
};

const base = '/mnt/data/predictive-maintenance-project';
const assets = `${base}/assets`;

function addHeader(slide, title, subtitle='') {
  slide.addText(title, { x:0.55, y:0.36, w:8.2, h:0.42, fontFace:'Aptos Display', fontSize:28, bold:true, color:theme.ink });
  if (subtitle) slide.addText(subtitle, { x:0.55, y:0.78, w:8.5, h:0.28, fontFace:'Aptos', fontSize:12.5, color:theme.muted });
}
function addFooter(slide, txt='Synthetic demo project • portfolio-ready starter package') {
  slide.addText(txt, { x:0.55, y:7.03, w:6.8, h:0.18, fontFace:'Aptos', fontSize:9.5, color:'7B8794' });
  slide.addText('Vincent Eng', { x:11.7, y:7.03, w:1.1, h:0.18, align:'right', fontFace:'Aptos', fontSize:9.5, color:'7B8794' });
}
function addMetricCard(slide, x, y, w, h, label, value, accent) {
  slide.addShape(pptx.ShapeType.roundRect, { x, y, w, h, rectRadius:0.08, fill:{ color:'FFFFFF' }, line:{ color:theme.line, width:1 }, shadow:safeOuterShadow('000000',0.12,45,1,0.5)});
  slide.addText(label, { x:x+0.18, y:y+0.18, w:w-0.36, h:0.18, fontSize:10.5, color:theme.muted, bold:true });
  slide.addText(value, { x:x+0.18, y:y+0.42, w:w-0.36, h:0.36, fontFace:'Aptos Display', fontSize:24, color:accent || theme.ink, bold:true });
}

// Slide 1
{
  const slide = pptx.addSlide();
  slide.background = { color: theme.dark };
  slide.addImage({ path: `${assets}/temp_vibration_scatter.png`, transparency: 12, ...imageSizingCrop(`${assets}/temp_vibration_scatter.png`, 7.0, 0.0, 6.33, 7.5) });
  slide.addShape(pptx.ShapeType.rect, { x:0, y:0, w:13.33, h:7.5, fill:{ color:'07151D', transparency:18 }, line:{ color:'07151D', transparency:100 } });
  slide.addShape(pptx.ShapeType.roundRect, { x:0.7, y:0.9, w:2.2, h:0.38, rectRadius:0.08, fill:{ color:theme.teal }, line:{ color:theme.teal } });
  slide.addText('SMART MANUFACTURING AI USE CASE', { x:0.94, y:0.995, w:1.8, h:0.14, fontFace:'Aptos', fontSize:10, bold:true, color:theme.white, align:'center' });
  slide.addText('Predictive\nMaintenance', { x:0.72, y:1.55, w:5.4, h:1.6, fontFace:'Aptos Display', fontSize:28, bold:true, color:theme.white });
  slide.addText('A portfolio-ready starter project with synthetic machine data, Python model training code, and an executive slide deck.', { x:0.75, y:3.35, w:4.85, h:0.9, fontFace:'Aptos', fontSize:18, color:'D9E2EC' });
  addMetricCard(slide, 0.78, 4.7, 1.75, 1.05, 'Dataset', '1,200 rows', theme.teal2);
  addMetricCard(slide, 2.68, 4.7, 1.55, 1.05, 'Model', 'RF', theme.blue);
  addMetricCard(slide, 4.38, 4.7, 1.55, 1.05, 'AUC', '0.772', theme.orange);
  slide.addText('Designed to show how IT, OT, and maintenance teams can move from reactive repair to risk-based intervention.', { x:0.8, y:6.15, w:5.3, h:0.42, fontFace:'Aptos', fontSize:12.5, color:'BCCCDC' });
  slide.addNotes(`[Sources]\n- All metrics and visuals are generated from the synthetic sample dataset bundled with this project.`);
}

// Slide 2
{
  const slide = pptx.addSlide();
  slide.background = { color: theme.bg };
  addHeader(slide, 'Why this use case matters', 'Move maintenance from calendar-driven tasks to probability-driven intervention.');
  slide.addShape(pptx.ShapeType.roundRect, { x:0.55, y:1.28, w:4.18, h:5.25, rectRadius:0.06, fill:{ color:'FFFFFF' }, line:{ color:theme.line } });
  slide.addText('Business pain points', { x:0.82, y:1.55, w:2.2, h:0.22, fontSize:18, bold:true, color:theme.ink });
  const bullets = [
    'Unexpected asset failure causes missed output and overtime labor.',
    'Maintenance planners do not have a ranked list of at-risk machines.',
    'Sensor signals exist, but they are not converted into timely alerts.',
    'The goal is to predict failure in the next 7 days and prioritize action.'
  ];
  slide.addText(bullets.map(t=>({text:t, options:{bullet:{indent:14}}})), { x:0.85, y:1.95, w:3.45, h:2.2, fontSize:15.5, color:theme.ink, breakLine:true, paraSpaceAfterPt:10 });
  slide.addShape(pptx.ShapeType.roundRect, { x:0.85, y:4.55, w:3.3, h:1.4, rectRadius:0.05, fill:{ color:'E6FFFB' }, line:{ color:'B2F5EA' } });
  slide.addText('Target KPI', { x:1.05, y:4.8, w:1.1, h:0.18, fontSize:11, color:theme.muted, bold:true });
  slide.addText('↓ unplanned downtime\n↑ maintenance efficiency', { x:1.05, y:5.05, w:2.5, h:0.5, fontSize:21, color:theme.teal, bold:true });

  slide.addShape(pptx.ShapeType.roundRect, { x:4.95, y:1.28, w:3.86, h:2.5, rectRadius:0.06, fill:{ color:'FFFFFF' }, line:{ color:theme.line } });
  slide.addText('Failure rate by line', { x:5.18, y:1.53, w:1.8, h:0.18, fontSize:17, bold:true, color:theme.ink });
  slide.addImage({ path: `${assets}/failure_rate_by_line.png`, ...imageSizingContain(`${assets}/failure_rate_by_line.png`, 5.08, 1.82, 3.55, 1.7) });

  slide.addShape(pptx.ShapeType.roundRect, { x:8.98, y:1.28, w:3.8, h:2.5, rectRadius:0.06, fill:{ color:'FFFFFF' }, line:{ color:theme.line } });
  slide.addText('Illustrative downtime cost', { x:9.2, y:1.53, w:2.4, h:0.18, fontSize:17, bold:true, color:theme.ink });
  slide.addImage({ path: `${assets}/downtime_cost.png`, ...imageSizingContain(`${assets}/downtime_cost.png`, 9.12, 1.82, 3.5, 1.7) });

  addMetricCard(slide, 4.95, 4.1, 2.45, 1.1, 'Prediction window', 'Next 7 days', theme.teal);
  addMetricCard(slide, 7.55, 4.1, 2.45, 1.1, 'Signals used', '11 features', theme.blue);
  addMetricCard(slide, 10.15, 4.1, 2.63, 1.1, 'Starter outcome', 'Rank risk daily', theme.orange);
  slide.addText('This starter package uses synthetic sample data, so the cost chart is illustrative and intended for stakeholder storytelling.', { x:5.0, y:5.7, w:7.65, h:0.5, fontSize:12.2, color:theme.muted });
  addFooter(slide);
}

// Slide 3
{
  const slide = pptx.addSlide();
  slide.background = { color: theme.bg };
  addHeader(slide, 'Data signals and feature engineering', 'Blend sensor, process, and maintenance context into one machine-level record.');
  slide.addShape(pptx.ShapeType.roundRect, { x:0.55, y:1.28, w:4.0, h:5.2, rectRadius:0.06, fill:{ color:'FFFFFF' }, line:{ color:theme.line } });
  slide.addText('Signal categories', { x:0.82, y:1.55, w:1.7, h:0.2, fontSize:18, bold:true, color:theme.ink });
  slide.addImage({ path:'/mnt/data/industrial_sensors.png', ...imageSizingCrop('/mnt/data/industrial_sensors.png', 0.84, 1.9, 3.42, 1.65) });
  slide.addText([
    {text:'Sensor health: ', options:{bold:true,color:theme.ink}}, {text:'temperature, vibration, pressure, current\n', options:{color:theme.muted}},
    {text:'Process context: ', options:{bold:true,color:theme.ink}}, {text:'production line, line speed, shift\n', options:{color:theme.muted}},
    {text:'Maintenance state: ', options:{bold:true,color:theme.ink}}, {text:'days since maintenance, defect rate, energy spike'}
  ], { x:0.88, y:3.86, w:3.25, h:1.2, fontSize:14.4, breakLine:true });
  slide.addShape(pptx.ShapeType.roundRect, { x:0.86, y:5.3, w:3.25, h:0.82, rectRadius:0.05, fill:{ color:'F0FDF4' }, line:{ color:'C6F6D5' } });
  slide.addText('Label: failure_next_7d = 1 if the machine is expected to fail within 7 days.', { x:1.02, y:5.53, w:2.9, h:0.35, fontSize:13.2, color:'166534', bold:true });

  slide.addShape(pptx.ShapeType.roundRect, { x:4.78, y:1.28, w:3.88, h:2.45, rectRadius:0.06, fill:{ color:'FFFFFF' }, line:{ color:theme.line } });
  slide.addText('Sample rows', { x:5.02, y:1.53, w:1.3, h:0.2, fontSize:17, bold:true, color:theme.ink });
  slide.addText(`ID     Temp   Vib   Days  Line  Fail
M-008  78.8  5.73   104    B     1
M-021  67.4  4.02    19    A     0
M-044  82.1  6.11   131    C     1
M-055  71.3  4.66    42    A     0`, { x:5.05, y:1.98, w:3.25, h:1.35, fontFace:'Courier New', fontSize:11.6, color:theme.ink, breakLine:true, margin:0.02 });
  slide.addShape(pptx.ShapeType.roundRect, { x:8.88, y:1.28, w:3.92, h:2.45, rectRadius:0.06, fill:{ color:'FFFFFF' }, line:{ color:theme.line } });
  slide.addText('Risk pattern', { x:9.12, y:1.53, w:1.5, h:0.2, fontSize:17, bold:true, color:theme.ink });
  slide.addImage({ path: `${assets}/temp_vibration_scatter.png`, ...imageSizingContain(`${assets}/temp_vibration_scatter.png`, 9.02, 1.82, 3.6, 1.7) });

  slide.addText('Feature engineering flow', { x:5.03, y:4.24, w:2.2, h:0.2, fontSize:17, bold:true, color:theme.ink });
  slide.addShape(pptx.ShapeType.chevron, { x:6.58, y:5.07, w:0.42, h:0.3, fill:{ color:'B8C6DB' }, line:{ color:'B8C6DB' } });
  slide.addShape(pptx.ShapeType.chevron, { x:8.66, y:5.07, w:0.42, h:0.3, fill:{ color:'B8C6DB' }, line:{ color:'B8C6DB' } });
  slide.addShape(pptx.ShapeType.chevron, { x:10.67, y:5.07, w:0.42, h:0.3, fill:{ color:'B8C6DB' }, line:{ color:'B8C6DB' } });
  [
    [5.02,'Raw signals','Sensors\nCMMS\nMES'],
    [7.1,'Cleaning','Missing values\ncaps\nunit checks'],
    [9.18,'Features','lags\nrolling stats\nrisk flags'],
    [11.19,'Label set','7-day failure\nclassification']
  ].forEach(([x, title, body], idx) => {
    slide.addShape(pptx.ShapeType.roundRect, { x, y:4.78, w:1.48, h:1.05, rectRadius:0.05, fill:{ color: idx===2 ? 'E6FFFB' : 'F8FAFC' }, line:{ color: idx===2 ? '5EEAD4' : theme.line } });
    slide.addText(title, { x:x+0.10, y:4.93, w:1.28, h:0.2, fontSize:12.6, bold:true, align:'center', color:theme.ink });
    slide.addText(body, { x:x+0.10, y:5.18, w:1.28, h:0.48, fontSize:10.4, align:'center', color:theme.muted });
  });
  slide.addNotes(`[Sources]\n- Industrial sensors image: https://www.st.com/en/applications/factory-automation/industrial-sensors.html\n- All charts and table values are generated from the synthetic sample dataset bundled with this project.`);
  addFooter(slide);
}

// Slide 4
{
  const slide = pptx.addSlide();
  slide.background = { color: theme.bg };
  addHeader(slide, 'Model approach and starter results', 'A random forest baseline produces a ranked risk score and interpretable feature importance.');
  addMetricCard(slide, 0.58, 1.28, 1.85, 1.05, 'ROC AUC', '0.772', theme.blue);
  addMetricCard(slide, 2.58, 1.28, 1.85, 1.05, 'Precision', '0.677', theme.teal);
  addMetricCard(slide, 4.58, 1.28, 1.85, 1.05, 'Recall', '0.757', theme.orange);
  addMetricCard(slide, 6.58, 1.28, 1.85, 1.05, 'F1 score', '0.715', '7C3AED');
  slide.addShape(pptx.ShapeType.roundRect, { x:0.55, y:2.65, w:5.98, h:3.58, rectRadius:0.06, fill:{ color:'FFFFFF' }, line:{ color:theme.line } });
  slide.addText('Top predictive signals', { x:0.84, y:2.92, w:2.1, h:0.2, fontSize:18, bold:true, color:theme.ink });
  slide.addImage({ path: `${assets}/feature_importance.png`, ...imageSizingContain(`${assets}/feature_importance.png`, 0.82, 3.22, 5.42, 2.63) });

  slide.addShape(pptx.ShapeType.roundRect, { x:6.78, y:2.65, w:2.68, h:3.58, rectRadius:0.06, fill:{ color:'FFFFFF' }, line:{ color:theme.line } });
  slide.addText('Confusion matrix', { x:7.03, y:2.92, w:1.6, h:0.2, fontSize:18, bold:true, color:theme.ink });
  slide.addImage({ path: `${assets}/confusion_matrix.png`, ...imageSizingContain(`${assets}/confusion_matrix.png`, 7.08, 3.3, 2.12, 2.45) });

  slide.addShape(pptx.ShapeType.roundRect, { x:9.7, y:2.65, w:3.1, h:3.58, rectRadius:0.06, fill:{ color:'FFFFFF' }, line:{ color:theme.line } });
  slide.addText('What this means', { x:9.96, y:2.92, w:1.7, h:0.2, fontSize:18, bold:true, color:theme.ink });
  slide.addText([
    {text:'Strongest synthetic drivers: ', options:{bold:true,color:theme.ink}},
    {text:'vibration, temperature, days since maintenance, current, and line speed.\n\n', options:{color:theme.muted}},
    {text:'Use case value: ', options:{bold:true,color:theme.ink}},
    {text:'maintenance can review the top-risk machines daily instead of treating every asset the same.\n\n', options:{color:theme.muted}},
    {text:'Next improvement: ', options:{bold:true,color:theme.ink}},
    {text:'add time-series drift features and machine-specific thresholds.', options:{color:theme.muted}},
  ], { x:9.95, y:3.22, w:2.58, h:2.62, fontSize:13.4, breakLine:true });
  addFooter(slide);
}

// Slide 5
{
  const slide = pptx.addSlide();
  slide.background = { color: theme.bg };
  addHeader(slide, 'From model output to maintenance action', 'Operationalize the score through a simple data and alerting pipeline.');
  slide.addShape(pptx.ShapeType.roundRect, { x:0.55, y:1.3, w:8.15, h:5.15, rectRadius:0.06, fill:{ color:'FFFFFF' }, line:{ color:theme.line } });
  slide.addText('Deployment architecture', { x:0.84, y:1.58, w:2.2, h:0.2, fontSize:18, bold:true, color:theme.ink });
  slide.addShape(pptx.ShapeType.chevron, { x:2.38, y:3.75, w:0.46, h:0.34, fill:{ color:'B8C6DB' }, line:{ color:'B8C6DB' } });
  slide.addShape(pptx.ShapeType.chevron, { x:4.38, y:3.75, w:0.46, h:0.34, fill:{ color:'B8C6DB' }, line:{ color:'B8C6DB' } });
  slide.addShape(pptx.ShapeType.chevron, { x:6.38, y:3.75, w:0.46, h:0.34, fill:{ color:'B8C6DB' }, line:{ color:'B8C6DB' } });
  [
    [0.88, 'Edge data', 'PLC / sensor\ntelemetry'],
    [2.88, 'Ingestion', 'Historian /\ndata lake'],
    [4.88, 'Scoring', 'Batch job or\nAPI model'],
    [6.88, 'Action', 'CMMS ticket\n& alert list']
  ].forEach(([x,title,body], idx) => {
    slide.addShape(pptx.ShapeType.roundRect, { x, y:3.28, w:1.48, h:1.05, rectRadius:0.05, fill:{ color: idx===2 ? 'EAF2FF' : 'F8FAFC' }, line:{ color: idx===2 ? '93C5FD' : theme.line } });
    slide.addText(title, { x:x+0.11, y:3.48, w:1.25, h:0.18, fontSize:12.6, bold:true, align:'center', color:theme.ink });
    slide.addText(body, { x:x+0.11, y:3.72, w:1.25, h:0.42, fontSize:10.6, align:'center', color:theme.muted });
  });
  slide.addText('Suggested operating rhythm', { x:0.88, y:2.13, w:2.2, h:0.2, fontSize:16.5, bold:true, color:theme.ink });
  slide.addText([
    {text:'1. ', options:{bold:true,color:theme.teal}}, {text:'Ingest machine and maintenance records daily.\n', options:{color:theme.muted}},
    {text:'2. ', options:{bold:true,color:theme.teal}}, {text:'Score each machine and rank the top 10 risks per line.\n', options:{color:theme.muted}},
    {text:'3. ', options:{bold:true,color:theme.teal}}, {text:'Review in morning maintenance huddle.\n', options:{color:theme.muted}},
    {text:'4. ', options:{bold:true,color:theme.teal}}, {text:'Feed outcomes back to improve thresholds and labels.', options:{color:theme.muted}}
  ], { x:0.88, y:2.44, w:6.9, h:0.62, fontSize:13.2, breakLine:true });

  slide.addShape(pptx.ShapeType.roundRect, { x:8.95, y:1.3, w:3.85, h:5.15, rectRadius:0.06, fill:{ color:'FFFFFF' }, line:{ color:theme.line } });
  slide.addImage({ path:'/mnt/data/pm_technician.png', ...imageSizingCrop('/mnt/data/pm_technician.png', 9.18, 1.58, 3.4, 2.25) });
  slide.addText('Decision support output', { x:9.18, y:4.06, w:2.3, h:0.2, fontSize:17, bold:true, color:theme.ink });
  slide.addText([
    {text:'Machine M-044\n', options:{bold:true,color:theme.ink}},
    {text:'Risk score 0.84 • Line C\nHigh vibration + overdue maintenance\nSuggested action: inspect bearings and review spare-part stock.', options:{color:theme.muted}}
  ], { x:9.18, y:4.38, w:3.15, h:1.05, fontSize:14, breakLine:true });
  slide.addShape(pptx.ShapeType.roundRect, { x:9.18, y:5.55, w:1.6, h:0.44, rectRadius:0.05, fill:{ color:'DBEAFE' }, line:{ color:'DBEAFE' } });
  slide.addShape(pptx.ShapeType.roundRect, { x:10.95, y:5.55, w:1.4, h:0.44, rectRadius:0.05, fill:{ color:'E6FFFB' }, line:{ color:'E6FFFB' } });
  slide.addText('Create ticket', { x:9.41, y:5.68, w:1.1, h:0.12, fontSize:11.2, bold:true, color:theme.blue });
  slide.addText('Notify planner', { x:11.13, y:5.68, w:1.0, h:0.12, fontSize:11.2, bold:true, color:theme.teal });
  slide.addNotes(`[Sources]\n- Technician image: https://auto.edu/industrial-maintenance`);
  addFooter(slide);
}

// Slide 6
{
  const slide = pptx.addSlide();
  slide.background = { color: theme.bg };
  addHeader(slide, 'Project package and next steps', 'Everything included to turn this into a portfolio project or a plant pilot.');
  const cards = [
    [0.7,1.45,'README','Business problem, data dictionary, results, and extension ideas.'],
    [3.42,1.45,'Python code','Training script with model fit, metrics, and output charts.'],
    [6.14,1.45,'Sample data','Synthetic machine sensor dataset with failure labels.'],
    [8.86,1.45,'Slides','Executive-ready story for AI + maintenance stakeholders.']
  ];
  cards.forEach(([x,y,title,body],i)=>{
    slide.addShape(pptx.ShapeType.roundRect,{x,y,w:2.35,h:1.7,rectRadius:0.06,fill:{color:'FFFFFF'},line:{color:theme.line}});
    slide.addText(title,{x:x+0.16,y:y+0.2,w:1.7,h:0.22,fontSize:18,bold:true,color:[theme.teal,theme.blue,theme.orange,'7C3AED'][i]});
    slide.addText(body,{x:x+0.16,y:y+0.55,w:1.95,h:0.7,fontSize:13.2,color:theme.muted});
  });
  slide.addShape(pptx.ShapeType.roundRect, { x:0.7, y:3.65, w:5.55, h:2.1, rectRadius:0.06, fill:{ color:'FFFFFF' }, line:{ color:theme.line } });
  slide.addText('How to strengthen this project', { x:0.95, y:3.93, w:2.8, h:0.2, fontSize:18, bold:true, color:theme.ink });
  slide.addText([
    {text:'• Replace synthetic labels with real work-order outcomes.\n', options:{color:theme.muted}},
    {text:'• Add rolling-window features from historian data.\n', options:{color:theme.muted}},
    {text:'• Compare random forest with XGBoost or temporal models.\n', options:{color:theme.muted}},
    {text:'• Integrate outputs with CMMS and planner dashboards.', options:{color:theme.muted}}
  ], { x:0.98, y:4.28, w:4.85, h:1.1, fontSize:14, breakLine:true });

  slide.addShape(pptx.ShapeType.roundRect, { x:6.55, y:3.65, w:6.05, h:2.1, rectRadius:0.06, fill:{ color:'0F766E' }, line:{ color:'0F766E' } });
  slide.addText('Suggested portfolio headline', { x:6.88, y:3.95, w:2.8, h:0.2, fontSize:18, bold:true, color:'DFFCF7' });
  slide.addText('Built an end-to-end predictive maintenance starter project for smart manufacturing, covering data design, model training, stakeholder storytelling, and deployment architecture.', { x:6.88, y:4.32, w:5.2, h:0.78, fontSize:20, bold:true, color:'FFFFFF' });
  slide.addText('Use this as a base repo for CIO / Head of IT / Digital Transformation interviews.', { x:6.88, y:5.18, w:4.9, h:0.24, fontSize:12.5, color:'CFFAFE' });
  addFooter(slide, 'Starter project includes code, sample data, README, and executive deck');
}

for (const s of pptx._slides) {
  warnIfSlideHasOverlaps(s, pptx);
  warnIfSlideElementsOutOfBounds(s, pptx);
}

pptx.writeFile({ fileName: `${base}/predictive_maintenance_project_deck.pptx` });
