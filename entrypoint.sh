#!/bin/sh
python aws_pricing.py | jq -s -r '
  "Region\tInstance\tPrice Category\tOS\tPrice (USD/Hr)\tDescription\tEffective Date",
  (
    .[] as $root
    | (
        ["OnDemand"][] as $termType
        | if ($root.terms[$termType]) then
            $root.terms[$termType] | to_entries[]
            | . as $entry
            | (
                $entry.value.priceDimensions | to_entries[0] as $pd
                | {
                    region: $root.region_code,
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
    | select(
         (.description | test("On Demand")
          and (test("Unused Reservation") | not)
          and (test("\\$0\\.00 per Reservation") | not)
          and (test("Linux with SQL") | not ))
         and (.os == "Linux")
       )
    | "\(.region)\t\(.instance)\t\(.priceCategory)\t\(.os)\t\(.price)\t\(.description)\t\(.effectiveDate)"
  )
'
