"""
Internationalization (i18n) module for C25K Calendar Creator.
Provides multi-language support for the application interface and content.
"""

from typing import Dict, Any
import json


class LanguageManager:
    """Manages translations and localization for the application"""
    
    def __init__(self):
        self.current_language = "en"
        self.translations = {}
        self.supported_languages = {
            "en": "English",
            "es": "Español",
            "fr": "Français", 
            "de": "Deutsch",
            "pt": "Português"
        }
        self._load_translations()
    
    def _load_translations(self):
        """Load all translation files"""
        # English (default)
        self.translations["en"] = {
            "app_title": "C25K Calendar Creator",
            "welcome": "Welcome to your personalized Couch to 5K journey!",
            "week": "Week",
            "day": "Day",
            "session": "Session",
            "warmup": "Warm-up",
            "cooldown": "Cool-down",
            "run": "Run",
            "walk": "Walk",
            "minutes": "minutes",
            "seconds": "seconds",
            "rest_day": "Rest Day",
            "workout_complete": "Workout Complete!",
            "congratulations": "Congratulations!",
            "export_formats": {
                "ics": "Calendar (ICS)",
                "excel": "Excel Tracker",
                "csv": "CSV Spreadsheet",
                "json": "JSON Data",
                "markdown": "Markdown Checklist",
                "pdf": "PDF Guide",
                "qr": "QR Code"
            },
            "tips": {
                "hydration": "Stay hydrated before, during, and after running",
                "pace": "Start slow and focus on endurance, not speed",
                "rest": "Rest days are just as important as workout days",
                "consistency": "Consistency is more important than intensity"
            },
            "safety": {
                "medical_disclaimer": "This application is for informational purposes only. Consult your healthcare provider before starting any new exercise program.",
                "listen_to_body": "Listen to your body and rest when needed",
                "proper_footwear": "Proper footwear is essential for injury prevention"
            },
            "weather": {
                "perfect": "Perfect weather for running!",
                "hot": "Hot weather - run early morning/evening, stay hydrated",
                "cold": "Cool weather - perfect for running! Dress in layers",
                "rain": "Consider indoor training or postpone to avoid safety risks",
                "windy": "Windy conditions - adjust pace, start into the wind"
            },
            "gui": {
                "name": "Name",
                "age": "Age",
                "weight": "Weight",
                "height": "Height",
                "start_date": "Start Date",
                "session_time": "Session Time",
                "generate_plan": "Generate C25K Plan",
                "export_plan": "Export Plan",
                "settings": "Settings",
                "language": "Language",
                "units": "Units",
                "accessibility": "Accessibility",
                "high_contrast": "High Contrast Mode",
                "large_font": "Large Font",
                "screen_reader": "Screen Reader Support"
            }
        }
        
        # Spanish translations
        self.translations["es"] = {
            "app_title": "Creador de Calendario C25K",
            "welcome": "¡Bienvenido a tu viaje personalizado de Sofá a 5K!",
            "week": "Semana",
            "day": "Día", 
            "session": "Sesión",
            "warmup": "Calentamiento",
            "cooldown": "Enfriamiento",
            "run": "Correr",
            "walk": "Caminar",
            "minutes": "minutos",
            "seconds": "segundos",
            "rest_day": "Día de Descanso",
            "workout_complete": "¡Entrenamiento Completo!",
            "congratulations": "¡Felicitaciones!",
            "export_formats": {
                "ics": "Calendario (ICS)",
                "excel": "Rastreador Excel",
                "csv": "Hoja de Cálculo CSV",
                "json": "Datos JSON",
                "markdown": "Lista Markdown",
                "pdf": "Guía PDF",
                "qr": "Código QR"
            },
            "tips": {
                "hydration": "Mantente hidratado antes, durante y después de correr",
                "pace": "Comienza despacio y enfócate en la resistencia, no en la velocidad",
                "rest": "Los días de descanso son tan importantes como los días de entrenamiento",
                "consistency": "La consistencia es más importante que la intensidad"
            },
            "safety": {
                "medical_disclaimer": "Esta aplicación es solo para fines informativos. Consulta a tu proveedor de atención médica antes de comenzar cualquier nuevo programa de ejercicios.",
                "listen_to_body": "Escucha a tu cuerpo y descansa cuando sea necesario",
                "proper_footwear": "El calzado adecuado es esencial para la prevención de lesiones"
            },
            "weather": {
                "perfect": "¡Clima perfecto para correr!",
                "hot": "Clima caliente - corre temprano por la mañana/tarde, mantente hidratado",
                "cold": "Clima fresco - ¡perfecto para correr! Vístete en capas",
                "rain": "Considera entrenamiento bajo techo o pospone para evitar riesgos de seguridad",
                "windy": "Condiciones ventosas - ajusta el ritmo, comienza contra el viento"
            },
            "gui": {
                "name": "Nombre",
                "age": "Edad",
                "weight": "Peso",
                "height": "Altura",
                "start_date": "Fecha de Inicio",
                "session_time": "Hora de Sesión",
                "generate_plan": "Generar Plan C25K",
                "export_plan": "Exportar Plan",
                "settings": "Configuración",
                "language": "Idioma",
                "units": "Unidades",
                "accessibility": "Accesibilidad",
                "high_contrast": "Modo de Alto Contraste",
                "large_font": "Fuente Grande",
                "screen_reader": "Soporte para Lector de Pantalla"
            }
        }
        
        # French translations
        self.translations["fr"] = {
            "app_title": "Créateur de Calendrier C25K",
            "welcome": "Bienvenue dans votre parcours personnalisé Canapé vers 5K!",
            "week": "Semaine",
            "day": "Jour",
            "session": "Séance",
            "warmup": "Échauffement",
            "cooldown": "Récupération",
            "run": "Courir",
            "walk": "Marcher",
            "minutes": "minutes",
            "seconds": "secondes",
            "rest_day": "Jour de Repos",
            "workout_complete": "Entraînement Terminé!",
            "congratulations": "Félicitations!",
            "export_formats": {
                "ics": "Calendrier (ICS)",
                "excel": "Suivi Excel",
                "csv": "Feuille de Calcul CSV",
                "json": "Données JSON",
                "markdown": "Liste Markdown",
                "pdf": "Guide PDF",
                "qr": "Code QR"
            },
            "tips": {
                "hydration": "Restez hydraté avant, pendant et après la course",
                "pace": "Commencez lentement et concentrez-vous sur l'endurance, pas la vitesse",
                "rest": "Les jours de repos sont aussi importants que les jours d'entraînement",
                "consistency": "La régularité est plus importante que l'intensité"
            },
            "safety": {
                "medical_disclaimer": "Cette application est à des fins informatives uniquement. Consultez votre professionnel de santé avant de commencer tout nouveau programme d'exercice.",
                "listen_to_body": "Écoutez votre corps et reposez-vous quand nécessaire",
                "proper_footwear": "Des chaussures appropriées sont essentielles pour la prévention des blessures"
            },
            "weather": {
                "perfect": "Temps parfait pour courir!",
                "hot": "Temps chaud - courez tôt le matin/soir, restez hydraté",
                "cold": "Temps frais - parfait pour courir! Habillez-vous en couches",
                "rain": "Considérez l'entraînement en intérieur ou reportez pour éviter les risques",
                "windy": "Conditions venteuses - ajustez le rythme, commencez face au vent"
            },
            "gui": {
                "name": "Nom",
                "age": "Âge",
                "weight": "Poids",
                "height": "Taille",
                "start_date": "Date de Début",
                "session_time": "Heure de Séance",
                "generate_plan": "Générer Plan C25K",
                "export_plan": "Exporter Plan",
                "settings": "Paramètres",
                "language": "Langue",
                "units": "Unités",
                "accessibility": "Accessibilité",
                "high_contrast": "Mode Contraste Élevé",
                "large_font": "Grande Police",
                "screen_reader": "Support Lecteur d'Écran"
            }
        }
    
    def set_language(self, language_code: str) -> bool:
        """Set the current language"""
        if language_code in self.supported_languages:
            self.current_language = language_code
            return True
        return False
    
    def get_text(self, key: str, *args) -> str:
        """Get translated text for a key"""
        keys = key.split('.')
        text = self.translations.get(self.current_language, self.translations["en"])
        
        for k in keys:
            if isinstance(text, dict) and k in text:
                text = text[k]
            else:
                # Fallback to English if key not found
                fallback = self.translations["en"]
                for fk in keys:
                    if isinstance(fallback, dict) and fk in fallback:
                        fallback = fallback[fk]
                    else:
                        return f"[{key}]"  # Key not found
                return fallback
        
        # Format with arguments if provided
        if args and isinstance(text, str):
            try:
                return text.format(*args)
            except (IndexError, KeyError):
                return text
        
        return text if isinstance(text, str) else f"[{key}]"
    
    def get_available_languages(self) -> Dict[str, str]:
        """Get all available languages"""
        return self.supported_languages.copy()
    
    def get_current_language(self) -> str:
        """Get current language code"""
        return self.current_language
    
    def get_current_language_name(self) -> str:
        """Get current language name"""
        return self.supported_languages.get(self.current_language, "English")


class WorkoutTranslator:
    """Translates workout descriptions and instructions"""
    
    def __init__(self, language_manager: LanguageManager):
        self.lang_mgr = language_manager
        self._setup_workout_templates()
    
    def _setup_workout_templates(self):
        """Setup workout description templates for each language"""
        self.workout_templates = {
            "en": {
                "warmup_walk": "Warm up: {duration}-min brisk walk.",
                "cooldown_walk": "Cool down: {duration}-min walk.",
                "run_walk_intervals": "Run {run_time}, walk {walk_time} (repeat {repetitions} times).",
                "continuous_run": "Run {duration} min (no walking breaks!).",
                "mixed_intervals": "Run {run1} min, walk {walk1} min, run {run2} min, walk {walk2} min, run {run3} min.",
                "graduation": "Graduation Day! Run {duration}+ min or 5K distance. Congratulations, you did it!"
            },
            "es": {
                "warmup_walk": "Calentamiento: caminata rápida de {duration} min.",
                "cooldown_walk": "Enfriamiento: caminata de {duration} min.",
                "run_walk_intervals": "Corre {run_time}, camina {walk_time} (repite {repetitions} veces).",
                "continuous_run": "Corre {duration} min (¡sin parar para caminar!).",
                "mixed_intervals": "Corre {run1} min, camina {walk1} min, corre {run2} min, camina {walk2} min, corre {run3} min.",
                "graduation": "¡Día de Graduación! Corre {duration}+ min o distancia 5K. ¡Felicitaciones, lo lograste!"
            },
            "fr": {
                "warmup_walk": "Échauffement: marche rapide de {duration} min.",
                "cooldown_walk": "Récupération: marche de {duration} min.",
                "run_walk_intervals": "Courez {run_time}, marchez {walk_time} (répétez {repetitions} fois).",
                "continuous_run": "Courez {duration} min (sans pauses de marche!).",
                "mixed_intervals": "Courez {run1} min, marchez {walk1} min, courez {run2} min, marchez {walk2} min, courez {run3} min.",
                "graduation": "Jour de Graduation! Courez {duration}+ min ou distance 5K. Félicitations, vous l'avez fait!"
            }
        }
    
    def translate_workout_description(self, week: int, day: int) -> str:
        """Generate translated workout description"""
        lang = self.lang_mgr.get_current_language()
        templates = self.workout_templates.get(lang, self.workout_templates["en"])
        
        # Get workout structure based on week and day
        workout_structure = self._get_workout_structure(week, day)
        
        description_parts = []
        
        # Warmup
        description_parts.append(templates["warmup_walk"].format(duration=5))
        
        # Main workout
        if workout_structure["type"] == "intervals":
            if workout_structure.get("mixed", False):
                description_parts.append(templates["mixed_intervals"].format(**workout_structure))
            else:
                description_parts.append(templates["run_walk_intervals"].format(**workout_structure))
        elif workout_structure["type"] == "continuous":
            if week == 10 and day == 3:  # Graduation day
                description_parts.append(templates["graduation"].format(**workout_structure))
            else:
                description_parts.append(templates["continuous_run"].format(**workout_structure))
        
        # Cooldown
        description_parts.append(templates["cooldown_walk"].format(duration=5))
        
        return " ".join(description_parts)
    
    def _get_workout_structure(self, week: int, day: int) -> Dict[str, Any]:
        """Get the structure of a specific workout"""
        # This mirrors the workout structure from core.py but focuses on the structure
        workout_structures = {
            1: {"type": "intervals", "run_time": "60 sec", "walk_time": "90 sec", "repetitions": 8},
            2: {"type": "intervals", "run_time": "90 sec", "walk_time": "2 min", "repetitions": 6},
            3: {"type": "intervals", "mixed": True, "run1": 1.5, "walk1": 1.5, "run2": 3, "walk2": 3, "run3": 1.5},
            4: {"type": "intervals", "mixed": True, "run1": 3, "walk1": 1.5, "run2": 5, "walk2": 2.5, "run3": 3},
            5: {
                1: {"type": "intervals", "mixed": True, "run1": 5, "walk1": 3, "run2": 5, "walk2": 3, "run3": 5},
                2: {"type": "intervals", "mixed": True, "run1": 8, "walk1": 5, "run2": 8, "walk2": 0, "run3": 0},
                3: {"type": "continuous", "duration": 20}
            },
            6: {
                1: {"type": "intervals", "mixed": True, "run1": 5, "walk1": 3, "run2": 8, "walk2": 3, "run3": 5},
                2: {"type": "intervals", "mixed": True, "run1": 10, "walk1": 3, "run2": 10, "walk2": 0, "run3": 0},
                3: {"type": "continuous", "duration": 25}
            },
            7: {"type": "continuous", "duration": 25},
            8: {"type": "continuous", "duration": 28},
            9: {"type": "continuous", "duration": 30},
            10: {"type": "continuous", "duration": 30}
        }
        
        week_structure = workout_structures.get(week, {"type": "continuous", "duration": 30})
        
        if isinstance(week_structure, dict) and "type" in week_structure:
            return week_structure
        elif isinstance(week_structure, dict) and day in week_structure:
            return week_structure[day]
        else:
            return {"type": "continuous", "duration": 30}
    
    def get_localized_tip(self, tip_key: str) -> str:
        """Get a localized tip"""
        return self.lang_mgr.get_text(f"tips.{tip_key}")
    
    def get_weather_advice(self, weather_condition: str) -> str:
        """Get localized weather advice"""
        return self.lang_mgr.get_text(f"weather.{weather_condition}")


class UnitsConverter:
    """Handle metric/imperial unit conversions and localization"""
    
    def __init__(self, language_manager: LanguageManager):
        self.lang_mgr = language_manager
        self.current_units = "metric"  # or "imperial"
    
    def set_units(self, units: str) -> bool:
        """Set current unit system"""
        if units in ["metric", "imperial"]:
            self.current_units = units
            return True
        return False
    
    def format_weight(self, weight_kg: float) -> str:
        """Format weight with appropriate units"""
        if self.current_units == "imperial":
            weight_lbs = weight_kg * 2.20462
            return f"{weight_lbs:.1f} lbs"
        else:
            return f"{weight_kg:.1f} kg"
    
    def format_height(self, height_cm: float) -> str:
        """Format height with appropriate units"""
        if self.current_units == "imperial":
            total_inches = height_cm / 2.54
            feet = int(total_inches // 12)
            inches = int(total_inches % 12)
            return f"{feet}'{inches}\""
        else:
            return f"{height_cm:.0f} cm"
    
    def format_distance(self, distance_km: float) -> str:
        """Format distance with appropriate units"""
        if self.current_units == "imperial":
            distance_miles = distance_km * 0.621371
            return f"{distance_miles:.2f} miles"
        else:
            return f"{distance_km:.2f} km"
    
    def format_pace(self, pace_min_per_km: float) -> str:
        """Format running pace with appropriate units"""
        if self.current_units == "imperial":
            pace_min_per_mile = pace_min_per_km * 1.609344
            minutes = int(pace_min_per_mile)
            seconds = int((pace_min_per_mile - minutes) * 60)
            return f"{minutes}:{seconds:02d}/mile"
        else:
            minutes = int(pace_min_per_km)
            seconds = int((pace_min_per_km - minutes) * 60)
            return f"{minutes}:{seconds:02d}/km"
    
    def format_temperature(self, temp_celsius: float) -> str:
        """Format temperature with appropriate units"""
        if self.current_units == "imperial":
            temp_fahrenheit = (temp_celsius * 9/5) + 32
            return f"{temp_fahrenheit:.0f}°F"
        else:
            return f"{temp_celsius:.0f}°C"


class InternationalizationManager:
    """Main class coordinating all internationalization features"""
    
    def __init__(self):
        self.language_manager = LanguageManager()
        self.workout_translator = WorkoutTranslator(self.language_manager)
        self.units_converter = UnitsConverter(self.language_manager)
    
    def set_language(self, language_code: str) -> bool:
        """Set the application language"""
        return self.language_manager.set_language(language_code)
    
    def set_units(self, units: str) -> bool:
        """Set the unit system"""
        return self.units_converter.set_units(units)
    
    def get_text(self, key: str, *args) -> str:
        """Get translated text"""
        return self.language_manager.get_text(key, *args)
    
    def get_translated_workout(self, week: int, day: int) -> str:
        """Get translated workout description"""
        return self.workout_translator.translate_workout_description(week, day)
    
    def format_user_data(self, user_data: Dict[str, Any]) -> Dict[str, str]:
        """Format user data with appropriate units and language"""
        formatted = {}
        
        if "weight" in user_data:
            formatted["weight"] = self.units_converter.format_weight(user_data["weight"])
        
        if "height" in user_data:
            formatted["height"] = self.units_converter.format_height(user_data["height"])
        
        # Add more formatting as needed
        return formatted
    
    def get_export_format_names(self) -> Dict[str, str]:
        """Get localized export format names"""
        return {
            "ics": self.get_text("export_formats.ics"),
            "excel": self.get_text("export_formats.excel"),
            "csv": self.get_text("export_formats.csv"),
            "json": self.get_text("export_formats.json"),
            "markdown": self.get_text("export_formats.markdown"),
            "pdf": self.get_text("export_formats.pdf"),
            "qr": self.get_text("export_formats.qr")
        }
    
    def get_available_languages(self) -> Dict[str, str]:
        """Get available languages"""
        return self.language_manager.get_available_languages()
    
    def get_current_language(self) -> str:
        """Get current language code"""
        return self.language_manager.get_current_language()
    
    def export_translations(self, filename: str) -> bool:
        """Export current translations to JSON file for external editing"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.language_manager.translations, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def import_translations(self, filename: str) -> bool:
        """Import translations from JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                imported_translations = json.load(f)
            
            # Validate and merge translations
            for lang_code, translations in imported_translations.items():
                if lang_code in self.language_manager.supported_languages:
                    self.language_manager.translations[lang_code] = translations
            
            return True
        except Exception:
            return False
