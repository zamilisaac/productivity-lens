# Initiative rubric: the fact questions (F1–F6)

Answer every question for every candidate initiative, **from the quote only**. Pick exactly one value
from each closed list. Never pick a value the quote does not support. If two values fit, or the quote is
unclear, set `uncertain = Y` and say why in `uncertain_reason`. Do not decide pass/fail, Tier, Grade or
Evidence type yourself: `classify.py` does that from these answers, using Playbook Module 2A.

Source of the rules: `docs/Productivity_Lens_Playbook_v1.12.md`, Module 2A, plus the Rules tab.

---

## F1 `category` – what kind of activity is it?

| Value | Use when | Examples |
| --- | --- | --- |
| `operations` | Anything done to run the business: lines, machines, systems, processes, layout, people's skills, distribution, sourcing, energy/water/waste in operations | new extrusion line; ERP; drive-in racking; multi-skilled operators |
| `csr` | Donations, community, scholarships, volunteering | school milk programme |
| `marketing` | Branding, campaigns, sponsorships, digital marketing | new brand campaign |
| `acquisition` | Buying or selling a company, plant, fleet or business | acquired a firm with 5 lines |
| `new_market` | Entering a new country, market or channel for the first time | export to China |
| `pricing_product` | Price changes, new products or flavours, product launches | launched oat milk |
| `hr_benefit` | Pay, allowances, retention perks, wellbeing, flexible hours, diversity, general safety programmes | wellness programme |
| `governance` | Board, policies, risk, audit, compliance systems, reporting | anti-bribery policy |

Training is `operations` (its result is judged in F3), unless it is a perk (then `hr_benefit`).

## F2 `status` – has the result happened in the period the report covers?

| Value | Use when |
| --- | --- |
| `achieved` | The quote describes something done, with a result already seen in the period |
| `planned` | "will", "plans to", "target", "expected", "aims to", "under construction", "to be commissioned", capacity not yet running |

## F3 `result_kind` – what is the reported result? (or, if no result, the stated purpose)

Pick the **strongest** result the quote actually states.

| Value | Meaning | Example quote |
| --- | --- | --- |
| `output_per_input` | Output or value added per worker, per machine hour, per unit of another input | "output per worker rose 15%" |
| `time` | Lead time, cycle time, delivery time, changeover time | "lead time cut from 5 to 3 days" |
| `cost` | Cost in RM (or cost per unit) saved or reduced | "saved RM1.2 million a year" |
| `quality_yield` | Defects, rejects, rework, yield, complaints per unit or period | "reject rate fell from 3% to 1%" |
| `downtime` | Machine downtime, stoppages, breakdowns | "downtime fell 20%" |
| `input_per_unit` | Energy, water, material, labour or space used per unit of output | "kWh per litre fell from 0.42 to 0.36" |
| `input_saving` | A total amount of an input saved or replaced (litres, kWh, kg), not per unit | "diesel use cut by 141,000 litres" |
| `utilisation` | Utilisation of an existing asset (racks, lines, trucks, space) | "rack utilisation up 13%" |
| `capacity` | Capacity or output volume of a line or plant, with no per-input measure | "70,000 to 180,000 pieces a day" |
| `investment_scale` | Size of what was installed or spent only | "12 robotic palletisers installed", "RM50m invested" |
| `revenue_profit` | Revenue, sales, profit, margin, market share | "plant revenue rose to RM31.9m" |
| `counts_scale` | Number of stores, outlets, customers, dealers, countries, herd, plantation, assets placed in market | "11,000 freezers placed" |
| `environmental_only` | Result only in environmental or social terms | "tCO2e avoided", "% renewable energy", "plastic reduced" |
| `compliance_award` | Certification, audits passed, awards, zero recalls/incidents, safety records | "ISO 22000 certified" |
| `training_hours` | Training hours or headcount trained, with no operating result | "5,868 training hours" |
| `none` | No result and no operating purpose stated | "we continue to improve efficiency" |

Notes:
- Water reused or waste recycled with no input saved (e.g. "581 million litres of effluent recycled") is `environmental_only`.
- Volume sold or produced for the whole company (e.g. litres sold) is `capacity`, not `output_per_input`.
- A cost **without** an RM figure ("lower distribution costs") is still `cost`; F5 records that no figure is given.
- Headcount reduction for the same output is `output_per_input` only if the quote links the two; otherwise `cost` or `none`.

## F4 `input` – which input does it change?

`people` · `machine_time` · `materials` · `energy` · `water` · `space` · `stock` · `none`

`none` means the quote gives no link to any input (Playbook question 1 fails).

## F5 `figure` – is the result quantified in the quote?

| Value | Use when |
| --- | --- |
| `before_after` | Both values given: "70,000 → 180,000", "from 4.02 to 3.66" |
| `single_impact` | One stated impact: "saved RM1.2m", "downtime fell 20%", "141,000 L diesel avoided" |
| `none` | No number for the result (a number for the investment size alone is still `none` here, unless F3 = `investment_scale`) |

## F6 `area` – where does it sit? (drives the Tier)

| Value | Tier | Covers |
| --- | --- | --- |
| `line_machinery` | 1 | new, faster or upgraded lines and machines |
| `automation_digital` | 1 | automation, robotics, digital systems, ERP, AI |
| `process_layout` | 1 | process redesign, lean, layout, storage layout (e.g. racking), debottlenecking, extra shifts |
| `capacity_existing_site` | 1 | capacity added **inside an existing site** |
| `consolidation` | 1 | closing or merging plants, warehouses or offices |
| `workforce_skills` | 1 | upskilling or multi-skilling used in operations, less reliance on low-cost labour |
| `distribution_restructure` | 1 | dealer, agent, route or fleet restructuring |
| `quality_yield` | 1 | quality, yield and rework programmes |
| `supply_chain_logistics` | 2 | sourcing, logistics, warehousing, localising production, resilience |
| `new_site` | 2 | a new plant or site (counts only once operating, with an operating result) |
| `resource` | 3 | water, waste, effluent, energy, material substitution |

Capacity at a **new** site is `new_site`, never `capacity_existing_site`.

## Other columns

- `source`: `AR` (annual report), `SR` (only in the sustainability statement or report – check the PageMap), `both`.
- `type`: initiative type for cross-company comparison (Playbook list): New/upgraded line · Automation/digital ·
  Process redesign · Capacity expansion · Facility consolidation · Workforce/skills · Distribution/channel ·
  Supply chain · Quality/yield · Resource substitution · Other.
- `rule` / `rule_outcome`: only when a Rules-tab rule settles this item (e.g. `R008`, `pass` or `fail`).

## Worked examples (from the Playbook table)

| Initiative (quote) | F1 | F2 | F3 | F4 | F5 | F6 | Engine result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Solar panels, "tCO2e avoided" | operations | achieved | environmental_only | energy | single_impact | resource | Not counted |
| Water recycling, "RM0.4m saved" | operations | achieved | cost | water | single_impact | resource | Tier 3 · A · Operating |
| Operators trained to run two lines | operations | achieved | none | people | none | workforce_skills | Tier 1 · C · Enabler |
| New plant revenue RM14.3m → RM31.9m | operations | achieved | revenue_profit | none | before_after | new_site | Not counted |
| New hub "expected to make 1 million pieces a day" | operations | planned | capacity | machine_time | single_impact | new_site | Not counted |
| Acquired a firm with 5 lines and 25 trucks | acquisition | achieved | counts_scale | none | single_impact | new_site | Not counted |
| 11,000 freezers placed with retailers | operations | achieved | counts_scale | none | single_impact | distribution_restructure | Not counted |
| Agents 971 → 252, distribution cost down RM2.1m | operations | achieved | cost | people | single_impact | distribution_restructure | Tier 1 · A · Operating |
| Drive-in racking raised rack utilisation 13% | operations | achieved | utilisation | space | single_impact | process_layout | Tier 1 · A · Operating |
| Second line: 70,000 → 180,000 pcs/day | operations | achieved | capacity | machine_time | before_after | capacity_existing_site | Tier 1 · A · Enabler |

## Rules-tab rules that affect the answers

| Rule | How to answer |
| --- | --- |
| R015 | Profit or segment change credited to "efficiency" with no action described → `result_kind = revenue_profit` |
| R016 | Capital work in progress or commitments with no project described → not a candidate; leave it out |
| R017 | Safety or equipment-handling training (forklift, reach truck, confined space) → `category = operations`, `area = workforce_skills`; shorter working day through process changes → `area = process_layout` |
| R032 / R033 | A headcount fall not linked by the company to the programme is not its result → `result_kind = none`, `figure = none` (Grade C) |
| R033 | No stated result → `figure = none`; the Grade stays C whatever the Tier |
| R036 | Too few lessons → add initiatives from the FY-2 and FY-4 annual reports, with the report year in `page` (e.g. `27 (FY2024 AR)`) |
| R040 | Disposal or consolidation → `area = consolidation`; it counts only with a productivity or operating result (engine rule) |
| R043 / R046 | A plant that **replaces** an existing one (all production moved, old plant closed) → `area = consolidation`, `rule = R046`, `rule_outcome = pass` (counts as a Tier 1 Enabler without an operating result) |
| R045 | No lesson qualifies after FY, FY-2 and FY-4 are searched → publish without lessons; never pad |
| R041 | Information too unclear to answer (e.g. a trial with no outcome) → `rule = R041`, `rule_outcome = skip` |
| R042 | Clearly environment-only results → `result_kind = environmental_only`; the engine keeps them out of every list |

Policy switches for these rules are at the top of `scripts/classify.py` (`POLICY`).
