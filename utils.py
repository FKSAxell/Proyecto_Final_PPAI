import pandas as pd
import streamlit as st

NUMERIC_COLS = [
    "Hours_Studied", "Attendance", "Sleep_Hours",
    "Previous_Scores", "Tutoring_Sessions", "Physical_Activity", "Exam_Score",
]
CATEGORICAL_COLS = [
    "Parental_Involvement", "Access_to_Resources", "Extracurricular_Activities",
    "Motivation_Level", "Internet_Access", "Family_Income", "Teacher_Quality",
    "School_Type", "Peer_Influence", "Learning_Disabilities",
    "Parental_Education_Level", "Distance_from_Home", "Gender",
]

COL_ES = {
    "Hours_Studied":              "Horas de estudio",
    "Attendance":                 "Asistencia (%)",
    "Sleep_Hours":                "Horas de sueño",
    "Previous_Scores":            "Puntajes anteriores",
    "Tutoring_Sessions":          "Sesiones de tutoría",
    "Physical_Activity":          "Actividad física (h/sem)",
    "Exam_Score":                 "Puntaje de examen",
    "Parental_Involvement":       "Involucramiento de padres",
    "Access_to_Resources":        "Acceso a recursos",
    "Extracurricular_Activities": "Actividades extracurriculares",
    "Motivation_Level":           "Nivel de motivación",
    "Internet_Access":            "Acceso a internet",
    "Family_Income":              "Ingreso familiar",
    "Teacher_Quality":            "Calidad docente",
    "School_Type":                "Tipo de colegio",
    "Peer_Influence":             "Influencia de pares",
    "Learning_Disabilities":      "Discapacidades de aprendizaje",
    "Parental_Education_Level":   "Nivel educativo de padres",
    "Distance_from_Home":         "Distancia al colegio",
    "Gender":                     "Género",
}

