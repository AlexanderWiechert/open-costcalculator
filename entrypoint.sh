#!/bin/sh
python aws_pricing.py | jq -s -r '
  "Instance\tPrice Category\tOS\tPrice (USD/Hr)\tDescription\tEffective Date",
  (
    .[] as $root
    | (
        # Wir betrachten nur OnDemand
        ["OnDemand"][] as $termType
        | if ($root.terms[$termType]) then
            $root.terms[$termType] | to_entries[]
            | . as $entry
            | (
                $entry.value.priceDimensions | to_entries[0] as $pd
                | {
                    instance: $root.product.attributes.instanceType,
                    priceCategory: $termType,
                    os: $root.product.attributes.operatingSystem,
                    price: $pd.value.pricePerUnit.USD,
                    description: $pd.value.description,
                    effectiveDate: $entry.value.effectiveDate
                }
            )
         else empty end
    )
    # Nur Einträge mit "On Demand" (aber nicht "Unused Reservation" oder "$0.00 per Reservation")
    | select(
         (.description | test("On Demand")
          and (test("Unused Reservation") | not)
          and (test("\\$0\\.00 per Reservation") | not)
          and (test("Linux with SQL") |not ))
         and (.os == "Linux")
       )
    # Falls mehrfach vorhanden, nehmen wir den ersten eindeutigen Eintrag
#    | unique_by(.description)
    | "\(.instance)\t\(.priceCategory)\t\(.os)\t\(.price)\t\(.description)\t\(.effectiveDate)"
  )
'
