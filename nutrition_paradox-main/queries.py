query_map = {
    # 🧋 Obesity Table (10 Queries)
    "Top 5 regions with highest average obesity (2022)": """
        SELECT "ParentLocation", AVG("NumericValue") AS avg_obesity
        FROM obesity
        WHERE "TimeDim" = 2022
        GROUP BY "ParentLocation"
        ORDER BY avg_obesity DESC
        LIMIT 5;
    """,
    "Top 5 countries with highest obesity estimates": """
        SELECT "SpatialDim", MAX("NumericValue") AS max_obesity
        FROM obesity
        GROUP BY "SpatialDim"
        ORDER BY max_obesity DESC
        LIMIT 5;
    """,
    "Obesity trend in India over years (Mean_estimate)": """
        SELECT "TimeDim", AVG("NumericValue") AS mean_obesity
        FROM obesity
        WHERE "SpatialDim" = 'IND'
        GROUP BY "TimeDim"
        ORDER BY "TimeDim";
    """,
    "Average obesity by gender": """
        SELECT "Dim1", AVG("NumericValue") AS avg_obesity
        FROM obesity
        GROUP BY "Dim1";
    """,
    "Country count by obesity level category and age group": """
        SELECT 
            CASE 
                WHEN "NumericValue" < 15 THEN 'Low'
                WHEN "NumericValue" BETWEEN 15 AND 30 THEN 'Medium'
                ELSE 'High'
            END AS obesity_level,
            "age_group",
            COUNT(DISTINCT "SpatialDim") AS country_count
        FROM obesity
        GROUP BY obesity_level, "age_group";
    """,
    "Top 5 least reliable and most consistent countries by CI_Width": """
        WITH ci_data AS (
            SELECT "SpatialDim", AVG("High" - "Low") AS CI_Width
            FROM obesity
            GROUP BY "SpatialDim"
        )
        SELECT * FROM (
            SELECT * FROM ci_data ORDER BY CI_Width DESC LIMIT 5
        )
        UNION ALL
        SELECT * FROM (
            SELECT * FROM ci_data ORDER BY CI_Width ASC LIMIT 5
        );
    """,
    "Average obesity by age group": """
        SELECT "age_group", AVG("NumericValue") AS avg_obesity
        FROM obesity
        GROUP BY "age_group";
    """,
    "Top 10 countries with consistently low obesity": """
        SELECT "SpatialDim", AVG("NumericValue") AS avg_obesity, AVG("High" - "Low") AS avg_CI
        FROM obesity
        GROUP BY "SpatialDim"
        HAVING avg_obesity < 15 AND avg_CI < 5
        ORDER BY avg_obesity ASC
        LIMIT 10;
    """,
    "Countries where female obesity exceeds male by large margin": """
        SELECT f."SpatialDim", f."TimeDim", f."NumericValue" AS female_obesity, m."NumericValue" AS male_obesity,
               f."NumericValue" - m."NumericValue" AS diff
        FROM obesity f
        JOIN obesity m ON f."SpatialDim" = m."SpatialDim" AND f."TimeDim" = m."TimeDim"
        WHERE f."Dim1" = 'SEX_FMLE' AND m."Dim1" = 'SEX_MLE'
        HAVING diff > 10
        ORDER BY diff DESC;
    """,
    "Global average obesity percentage per year": """
        SELECT "TimeDim", AVG("NumericValue") AS avg_obesity
        FROM obesity
        GROUP BY "TimeDim"
        ORDER BY "TimeDim";
    """,

    # 👾 Malnutrition Table (10 Queries)
    "Avg. malnutrition by age group": """
        SELECT "age_group", AVG("NumericValue") AS avg_malnutrition
        FROM malnutrition
        GROUP BY "age_group";
    """,
    "Top 5 countries with highest malnutrition": """
        SELECT "SpatialDim", MAX("NumericValue") AS max_malnutrition
        FROM malnutrition
        GROUP BY "SpatialDim"
        ORDER BY max_malnutrition DESC
        LIMIT 5;
    """,
    "Malnutrition trend in Africa over the years": """
        SELECT "TimeDim", AVG("NumericValue") AS avg_malnutrition
        FROM malnutrition
        WHERE "ParentLocation" = 'Africa'
        GROUP BY "TimeDim"
        ORDER BY "TimeDim";
    """,
    "Gender-based average malnutrition": """
        SELECT "Dim1", AVG("NumericValue") AS avg_malnutrition
        FROM malnutrition
        GROUP BY "Dim1";
    """,
    "Malnutrition CI_Width level-wise (by age group)": """
        SELECT "age_group", AVG("High" - "Low") AS avg_CI
        FROM malnutrition
        GROUP BY "age_group";
    """,
    "Yearly malnutrition in India, Nigeria, Brazil": """
        SELECT "SpatialDim", "TimeDim", AVG("NumericValue") AS avg_malnutrition
        FROM malnutrition
        WHERE "SpatialDim" IN ('IND', 'NGA', 'BRA')
        GROUP BY "SpatialDim", "TimeDim"
        ORDER BY "SpatialDim", "TimeDim";
    """,
    "Regions with lowest malnutrition averages": """
        SELECT "ParentLocation", AVG("NumericValue") AS avg_malnutrition
        FROM malnutrition
        GROUP BY "ParentLocation"
        ORDER BY avg_malnutrition ASC
        LIMIT 5;
    """,
    "Countries with increasing malnutrition": """
        SELECT "SpatialDim", MAX("NumericValue") - MIN("NumericValue") AS change
        FROM malnutrition
        GROUP BY "SpatialDim"
        HAVING change > 0
        ORDER BY change DESC;
    """,
    "Year-wise min/max malnutrition comparison": """
        SELECT "TimeDim", MIN("NumericValue") AS min_value, MAX("NumericValue") AS max_value
        FROM malnutrition
        GROUP BY "TimeDim"
        ORDER BY "TimeDim";
    """,
    "High CI_Width flags for monitoring": """
        SELECT "SpatialDim", "TimeDim", ("High" - "Low") AS CI_Width
        FROM malnutrition
        WHERE ("High" - "Low") > 5
        ORDER BY CI_Width DESC;
    """,

    # 🔗 Combined Queries (5 Queries)
    "Obesity vs malnutrition comparison (5 countries)": """
        SELECT o."SpatialDim", AVG(o."NumericValue") AS obesity_avg, AVG(m."NumericValue") AS malnutrition_avg
        FROM obesity o
        JOIN malnutrition m ON o."SpatialDim" = m."SpatialDim"
        WHERE o."SpatialDim" IN ('IND', 'USA', 'BRA', 'NGA', 'CHN')
        GROUP BY o."SpatialDim";
    """,
    "Gender disparity in both obesity and malnutrition": """
        SELECT o."Dim1", AVG(o."NumericValue") AS avg_obesity, AVG(m."NumericValue") AS avg_malnutrition
        FROM obesity o
        JOIN malnutrition m ON o."Dim1" = m."Dim1"
        GROUP BY o."Dim1";
    """,
    "Region-wise avg estimates (Africa and America)": """
        SELECT o."ParentLocation", AVG(o."NumericValue") AS obesity_avg, AVG(m."NumericValue") AS malnutrition_avg
        FROM obesity o
        JOIN malnutrition m ON o."ParentLocation" = m."ParentLocation"
        WHERE o."ParentLocation" IN ('Africa', 'Americas')
        GROUP BY o."ParentLocation";
    """,
    "Countries with obesity up & malnutrition down": """
        SELECT o."SpatialDim", 
               MAX(o."NumericValue") - MIN(o."NumericValue") AS obesity_change,
               MIN(m."NumericValue") - MAX(m."NumericValue") AS malnutrition_change
        FROM obesity o
        JOIN malnutrition m ON o."SpatialDim" = m."SpatialDim"
        GROUP BY o."SpatialDim"
        HAVING obesity_change > 0 AND malnutrition_change > 0;
    """,
    "Age-wise trend analysis": """
        SELECT o."age_group", AVG(o."NumericValue") AS obesity_avg, AVG(m."NumericValue") AS malnutrition_avg
        FROM obesity o
        JOIN malnutrition m ON o."age_group" = m."age_group"
        GROUP BY o."age_group";
    """
}
