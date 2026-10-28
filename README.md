# Nairobi Property Inquiry Extractor

This command-line script uses Anthropic to turn a raw property inquiry into a
validated Python dictionary, then prints each extracted field. It is intended
to help a property agent capture WhatsApp leads consistently instead of
copying details into a spreadsheet by hand.

## Extracted fields

| Field | Why it matters |
| --- | --- |
| `property_type` | Narrows the search to the kind of home requested, such as a house, apartment, or bedsitter. |
| `bedrooms` | Helps match the property's size to the client's needs; bedsitters are represented as `0`. |
| `location` | Identifies the Nairobi neighborhood or area for matching nearby listings. |
| `budget_kes` | Captures the client's price limit in Kenyan shillings, with shorthand such as `80k` normalized to `80000`. |
| `rental_or_sale` | Distinguishes a rental search from a purchase search. |

If a detail is missing or unclear, its value is `null` in the extracted
dictionary and is printed as `Not specified`.

## Setup

Use Python 3.10 or later. Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

Set `ANTHROPIC_API_KEY` in your environment or in a `.env` file in this
directory. The script loads `.env` automatically. Optionally set
`ANTHROPIC_MODEL` to override the default model (`claude-3-5-haiku-latest`).
Keep `.env` private; it is ignored by Git.

## Usage

```powershell
python day12_exercise.py "I am looking for a 3-bedroom house in Kileleshwa, budget around 80k per month"
```

You can also run the script without an argument and enter the message when
prompted. Output is printed one field per line.

## Example inquiries

1. `I am looking for a 3-bedroom house in Kileleshwa, budget around 80k per month`
2. `Do you have any bedsitters near Westlands under 20k?`
3. `I want to buy a 4-bedroom house in Karen for KES 35 million.`

The bedsitter inquiry demonstrates that an unstated sale/rental preference is
represented as `null`. Run the offline tests without making API
requests:

```powershell
python -m unittest -v
```
