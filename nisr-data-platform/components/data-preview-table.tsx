"use client"

import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"

export function DataPreviewTable() {
  // Sample data for preview
  const columns = [
    { name: "province", type: "string", description: "Province name" },
    { name: "district", type: "string", description: "District name" },
    { name: "sector", type: "string", description: "Sector name" },
    { name: "gender", type: "string", description: "Gender" },
    { name: "age_group", type: "string", description: "Age group" },
    { name: "education", type: "string", description: "Education level" },
    { name: "income", type: "number", description: "Monthly income (RWF)" },
    { name: "household_size", type: "number", description: "Number of household members" },
    { name: "has_electricity", type: "boolean", description: "Has electricity access" },
    { name: "has_water", type: "boolean", description: "Has clean water access" },
    { name: "has_internet", type: "boolean", description: "Has internet access" },
    { name: "survey_weight", type: "number", description: "Survey weight" },
  ]

  const data = [
    {
      province: "Kigali City",
      district: "Nyarugenge",
      sector: "Nyarugenge",
      gender: "Male",
      age_group: "25-34",
      education: "Secondary",
      income: 120000,
      household_size: 4,
      has_electricity: true,
      has_water: true,
      has_internet: true,
      survey_weight: 1.23,
    },
    {
      province: "Kigali City",
      district: "Nyarugenge",
      sector: "Nyarugenge",
      gender: "Female",
      age_group: "35-44",
      education: "University",
      income: 250000,
      household_size: 3,
      has_electricity: true,
      has_water: true,
      has_internet: true,
      survey_weight: 0.98,
    },
    {
      province: "Eastern",
      district: "Bugesera",
      sector: "Nyamata",
      gender: "Male",
      age_group: "45-54",
      education: "Primary",
      income: 75000,
      household_size: 6,
      has_electricity: true,
      has_water: false,
      has_internet: false,
      survey_weight: 1.45,
    },
    {
      province: "Eastern",
      district: "Bugesera",
      sector: "Nyamata",
      gender: "Female",
      age_group: "18-24",
      education: "Secondary",
      income: 60000,
      household_size: 5,
      has_electricity: true,
      has_water: true,
      has_internet: false,
      survey_weight: 1.12,
    },
    {
      province: "Northern",
      district: "Musanze",
      sector: "Kinigi",
      gender: "Male",
      age_group: "55+",
      education: "None",
      income: 45000,
      household_size: 4,
      has_electricity: false,
      has_water: true,
      has_internet: false,
      survey_weight: 1.78,
    },
  ]

  return (
    <div className="border rounded-md">
      <div className="border-b px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <h3 className="font-medium">Data Preview</h3>
          <p className="text-sm text-muted-foreground">Showing 5 of 1,245 rows</p>
        </div>
        <div className="flex gap-2">
          {["string", "number", "boolean"].map((type) => (
            <Badge key={type} variant="outline" className="capitalize">
              {type}
            </Badge>
          ))}
        </div>
      </div>
      <div className="overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow>
              {columns.map((column) => (
                <TableHead key={column.name} className="whitespace-nowrap">
                  <div className="font-medium">{column.name}</div>
                  <div className="text-xs text-muted-foreground">{column.type}</div>
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {data.map((row, rowIndex) => (
              <TableRow key={rowIndex}>
                {columns.map((column) => (
                  <TableCell key={`${rowIndex}-${column.name}`} className="whitespace-nowrap">
                    {typeof row[column.name as keyof typeof row] === "boolean"
                      ? row[column.name as keyof typeof row]
                        ? "Yes"
                        : "No"
                      : String(row[column.name as keyof typeof row])}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  )
}
