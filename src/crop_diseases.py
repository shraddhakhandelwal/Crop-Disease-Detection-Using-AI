"""
Crop and disease definitions for the detection system.
"""

CROP_DISEASES = {
    "tomato": {
        "early_blight": {
            "scientific_name": "Alternaria solani",
            "symptoms": [
                "Dark brown spots with concentric rings",
                "Yellowing around lesions",
                "Older leaves affected first"
            ],
            "treatments": {
                "low": {"pesticide": "Copper-based fungicide", "concentration": "0.1%"},
                "medium": {"pesticide": "Chlorothalonil", "concentration": "0.2%"},
                "high": {"pesticide": "Azoxystrobin", "concentration": "0.3%"}
            },
            "prevention": [
                "Crop rotation",
                "Proper plant spacing",
                "Drip irrigation"
            ]
        },
        "late_blight": {
            "scientific_name": "Phytophthora infestans",
            "symptoms": [
                "Water-soaked spots",
                "White fuzzy growth",
                "Dark brown lesions"
            ],
            "treatments": {
                "low": {"pesticide": "Mancozeb", "concentration": "0.15%"},
                "medium": {"pesticide": "Metalaxyl", "concentration": "0.25%"},
                "high": {"pesticide": "Cymoxanil", "concentration": "0.35%"}
            },
            "prevention": [
                "Plant resistant varieties",
                "Improve air circulation",
                "Avoid overhead irrigation"
            ]
        }
    },
    "potato": {
        "late_blight": {
            "scientific_name": "Phytophthora infestans",
            "symptoms": [
                "Dark brown spots on leaves",
                "White mold under leaves",
                "Rotting tubers"
            ],
            "treatments": {
                "low": {"pesticide": "Copper oxychloride", "concentration": "0.2%"},
                "medium": {"pesticide": "Mandipropamid", "concentration": "0.3%"},
                "high": {"pesticide": "Fluazinam", "concentration": "0.4%"}
            },
            "prevention": [
                "Use certified seed potatoes",
                "Plant in well-drained soil",
                "Proper hilling"
            ]
        },
        "scab": {
            "scientific_name": "Streptomyces scabies",
            "symptoms": [
                "Rough, corky patches on tubers",
                "Circular lesions",
                "Brown to tan coloration"
            ],
            "treatments": {
                "low": {"pesticide": "Sulfur-based treatment", "concentration": "0.2%"},
                "medium": {"pesticide": "Biological control agents", "concentration": "as directed"},
                "high": {"pesticide": "Integrated management", "concentration": "varies"}
            },
            "prevention": [
                "Maintain soil pH below 5.2",
                "Proper irrigation",
                "Resistant varieties"
            ]
        }
    },
    "corn": {
        "northern_leaf_blight": {
            "scientific_name": "Exserohilum turcicum",
            "symptoms": [
                "Long, elliptical gray-green lesions",
                "Lesions turn tan as they mature",
                "Start on lower leaves"
            ],
            "treatments": {
                "low": {"pesticide": "Propiconazole", "concentration": "0.1%"},
                "medium": {"pesticide": "Azoxystrobin", "concentration": "0.2%"},
                "high": {"pesticide": "Pyraclostrobin", "concentration": "0.3%"}
            },
            "prevention": [
                "Resistant hybrids",
                "Crop rotation",
                "Residue management"
            ]
        },
        "gray_leaf_spot": {
            "scientific_name": "Cercospora zeae-maydis",
            "symptoms": [
                "Rectangle-shaped lesions",
                "Gray to tan color",
                "Parallel leaf veins"
            ],
            "treatments": {
                "low": {"pesticide": "Chlorothalonil", "concentration": "0.15%"},
                "medium": {"pesticide": "Strobilurin", "concentration": "0.25%"},
                "high": {"pesticide": "Mixed-mode fungicides", "concentration": "0.35%"}
            },
            "prevention": [
                "Crop rotation",
                "Tillage practices",
                "Resistant varieties"
            ]
        }
    },
    "rice": {
        "blast": {
            "scientific_name": "Magnaporthe oryzae",
            "symptoms": [
                "Diamond-shaped lesions",
                "White to gray center",
                "Brown margins"
            ],
            "treatments": {
                "low": {"pesticide": "Tricyclazole", "concentration": "0.1%"},
                "medium": {"pesticide": "Isoprothiolane", "concentration": "0.2%"},
                "high": {"pesticide": "Azoxystrobin", "concentration": "0.3%"}
            },
            "prevention": [
                "Resistant varieties",
                "Silicon fertilization",
                "Water management"
            ]
        },
        "bacterial_blight": {
            "scientific_name": "Xanthomonas oryzae",
            "symptoms": [
                "Water-soaked yellowing",
                "Leaf curling",
                "White to yellow margins"
            ],
            "treatments": {
                "low": {"pesticide": "Copper oxychloride", "concentration": "0.2%"},
                "medium": {"pesticide": "Streptocycline", "concentration": "0.015%"},
                "high": {"pesticide": "Kasugamycin", "concentration": "0.3%"}
            },
            "prevention": [
                "Clean seed",
                "Balanced fertilization",
                "Field sanitation"
            ]
        }
    }
}