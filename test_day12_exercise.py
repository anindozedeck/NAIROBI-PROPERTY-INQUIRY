import json
import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from day12_exercise import (
    FIELDS,
    RESPONSE_SCHEMA,
    SYSTEM_PROMPT,
    extract_inquiry,
    print_fields,
)


class InquiryExtractionTests(unittest.TestCase):
    def test_extracts_three_inquiries_including_missing_information(self) -> None:
        examples = [
            (
                "I am looking for a 3-bedroom house in Kileleshwa, budget around 80k per month",
                {
                    "property_type": "house",
                    "bedrooms": 3,
                    "location": "Kileleshwa",
                    "budget_kes": 80000,
                    "rental_or_sale": "rental",
                },
            ),
            (
                "Do you have any bedsitters near Westlands under 20k?",
                {
                    "property_type": "bedsitter",
                    "bedrooms": 0,
                    "location": "Westlands",
                    "budget_kes": 20000,
                    "rental_or_sale": None,
                },
            ),
            (
                "I want to buy a 4-bedroom house in Karen for KES 35 million.",
                {
                    "property_type": "house",
                    "bedrooms": 4,
                    "location": "Karen",
                    "budget_kes": 35000000,
                    "rental_or_sale": "sale",
                },
            ),
        ]

        for inquiry, expected in examples:
            with self.subTest(inquiry=inquiry):
                client = Mock()
                client.messages.create.return_value = SimpleNamespace(
                    content=[SimpleNamespace(type="text", text=json.dumps(expected))]
                )

                result = extract_inquiry(inquiry, client)

                self.assertEqual(result, expected)
                self.assertEqual(tuple(result), FIELDS)
                request = client.messages.create.call_args.kwargs
                self.assertEqual(request["system"], SYSTEM_PROMPT)
                self.assertEqual(
                    request["output_config"]["format"]["schema"], RESPONSE_SCHEMA
                )
                self.assertEqual(request["messages"][0]["content"], inquiry)

    def test_prints_each_field_and_marks_missing_values(self) -> None:
        from io import StringIO
        from contextlib import redirect_stdout

        details = {
            "property_type": "bedsitter",
            "bedrooms": 0,
            "location": "Westlands",
            "budget_kes": 20000,
            "rental_or_sale": None,
        }
        output = StringIO()
        with redirect_stdout(output):
            print_fields(details)

        self.assertEqual(
            output.getvalue().splitlines(),
            [
                "Property Type: bedsitter",
                "Bedrooms: 0",
                "Location: Westlands",
                "Budget Kes: KES 20,000",
                "Rental Or Sale: Not specified",
            ],
        )


if __name__ == "__main__":
    unittest.main()
