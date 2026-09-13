# NYC Taxi Data Pipeline (Submission 2)

## Overview
โปรเจกต์นี้คือ Data Pipeline สำหรับการดึง ทำความสะอาด และวิเคราะห์ข้อมูล NYC Taxi เพื่อหาคำตอบว่ารถแท็กซี่ประเภทใดถูกใช้งานมากที่สุดในช่วงครึ่งปีแรกของปี 2024

## Pipeline / Data Flow Diagram
`mermaid
graph TD
    A[TLC Trip Record Data<br>URLs] -->|Extract| B(DuckDB)
    B -->|Transform / QA Check<br>Filter Date: Jan-Jun 2024| C[(Curated Data<br>Local Parquet Files)]
    C -->|Analyze| D[Result / Log Output<br>Most Used Taxi]
`
