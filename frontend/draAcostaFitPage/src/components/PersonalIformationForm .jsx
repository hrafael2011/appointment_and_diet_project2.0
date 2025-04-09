

import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { useFormik } from "formik";
import * as Yup from "yup";
import ReCAPTCHA from "react-google-recaptcha";
import { getCountries, getCitiesByCountry } from "../api/contries";
import { getPatientById, putPatient } from "../api/patient";

//const doctorId = 1;
const RECAPTCHA_SITE_KEY = "6LdYHOsqAAAAAFbDkivAKIBuZUF4cvSnt_whB2U5";

const PersonalInformationForm = () => {
    const{id} = useParams() // get the id from link
    const [isLoading, setIsLoading] = useState(true); // Estado para manejar la carga de datos
    const [formError, setFormError] = useState(null); // Estado para manejar errores al cargar datos

    const [message, setMessage] = useState(null);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [countries, setCountries] = useState([]);
    const [cities, setCities] = useState([]);
    const [loadingStates, setLoadingStates] = useState({
        countries: true,
        cities: false
    });

    const formik = useFormik({
        initialValues: {
            name: "",
            last_name: "",
            email: "",
            whatsapp: "",
            country: "",
            city: "",
            birthday: "",
            sex: "",
            weight: "",
            height: "",
            objetive: "",
            food_allergies: "",
            diseases: "",
            doctor: "",
            captcha: "",
        },
        validationSchema: Yup.object({
            name: Yup.string().required("El nombre es obligatorio").max(50, "Máximo 50 caracteres"),
            last_name: Yup.string().required("El apellido es obligatorio").max(50, "Máximo 50 caracteres"),
            email: Yup.string().email("Correo electrónico no válido").required("El correo electrónico es obligatorio"),
            whatsapp: Yup.string()
                .matches(/^\+?[0-9]{10,15}$/, "Número de teléfono no válido")
                .required("El número de teléfono es obligatorio"),
            country: Yup.string().required("El país es obligatorio"),
            city: Yup.string().required("La ciudad es obligatoria"),
            birthday: Yup.date().max(new Date(), "La fecha no puede ser futura").required("La fecha de nacimiento es obligatoria"),
            sex: Yup.string()
                .oneOf(['Masculino', 'Femenino'], 'Seleccione una opción válida')
                .required("El sexo es obligatorio"),
            weight: Yup.number()
                .typeError("Debe ser un número válido")
                .min(20, "El peso debe ser mayor a 20 lb")
                .max(600, "El peso debe ser menor a 600 lb")
                .required("El peso es obligatorio"),
            height: Yup.number()
                .typeError("Debe ser un número válido")
                .min(50, "La estatura debe ser mayor a 50 cm")
                .max(250, "La estatura debe ser menor a 250 cm")
                .required("La estatura es obligatoria"),
            objetive: Yup.string()
                .oneOf(["Bajar de peso", "Subir de peso"], "Seleccione una opción válida")
                .required("El objetivo es obligatorio"),
            food_allergies: Yup.string().max(500, "Máximo 500 caracteres"),
            diseases: Yup.string().max(500, "Máximo 500 caracteres"),
            captcha: Yup.string().required("Por favor, completa el CAPTCHA"),
        }),
        onSubmit: async (values, { resetForm }) => {
            console.group('Depuración antes de enviar');
            console.log('Valores del formulario:', JSON.parse(JSON.stringify(values)));
            
            // Verifica campos null/undefined
            const problematicFields = Object.entries(values)
                .filter(([key, value]) => value === null || value === undefined)
                .map(([key]) => key);
            
            if (problematicFields.length > 0) {
                console.error('Campos problemáticos:', problematicFields);
                setMessage({
                    type: "error",
                    text: `Los siguientes campos tienen valores inválidos: ${problematicFields.join(', ')}`
                });
                console.groupEnd();
                return;
            }
            console.groupEnd();
            try {
                setIsSubmitting(true);
                // Se asume que "id" está disponible en el componente (por ejemplo, obtenido con useParams)
                const response = await putPatient(id, values);
                console.log("Datos actualizados:", response);
                setMessage({
                    type: "success",
                    text: "Se ha actualizado la información del paciente.",
                });
                resetForm();
                setCities([]);
            } catch (error) {
                console.error("Error:", error);
                setMessage({
                    type: "error",
                    text: "Hubo un error al procesar su solicitud. Por favor, inténtelo de nuevo más tarde.",
                });
            } finally {
                setIsSubmitting(false);
            }
        },
        
    });

    const handleCaptchaChange = (value) => {
        formik.setFieldValue("captcha", value);
    };

    useEffect(() => {
        const fetchCountries = async () => {
            try {
                const countriesData = await getCountries();
                if (countriesData && Array.isArray(countriesData)) {
                    setCountries(countriesData);
                } else {
                    throw new Error("Formato de datos incorrecto");
                }
            } catch (error) {
                console.error("Error al cargar países:", error);
                setMessage({
                    type: "error",
                    text: "Error al cargar la lista de países. Por favor recargue la página.",
                });
            } finally {
                setLoadingStates(prev => ({...prev, countries: false}));
            }
        };
        
        fetchCountries();
    }, []);

    useEffect(() => {
        if (!formik.values.country) {
            setCities([]);
            formik.setFieldValue("city", "");
            return;
        }

        const timer = setTimeout(async () => {
            try {
                setLoadingStates(prev => ({...prev, cities: true}));
                const citiesData = await getCitiesByCountry(formik.values.country);
                setCities(citiesData || []);
                formik.setFieldValue("city", "");
            } catch (error) {
                console.error(`Error al obtener ciudades para ${formik.values.country}:`, error);
                setCities([]);
            } finally {
                setLoadingStates(prev => ({...prev, cities: false}));
            }
        }, 300);

        return () => clearTimeout(timer);
    }, [formik.values.country]);

    


    //

    useEffect(() => {
        const fetchPatientData = async () => {
            try {
                const patientData = await getPatientById(id);
                console.log('Datos recibidos de la API:', patientData); // ← Añade esto
                
                // Limpia los valores null/undefined
                const cleanedData = {};
                Object.keys(formik.initialValues).forEach(key => {
                    cleanedData[key] = patientData[key] ?? '';
                });
                
                console.log('Datos limpios para el formulario:', cleanedData); // ← Añade esto
                formik.setValues(cleanedData);
                setIsLoading(false);
            } catch (error) {
                console.error("Error al cargar los datos del paciente:", error);
                setFormError("No se pudo cargar la información del paciente.");
                setIsLoading(false);
            }
        };

        fetchPatientData();
    }, [id]);

    if (isLoading) {
        return <p>Cargando información del paciente...</p>;
    }

    if (formError) {
        return <p>{formError}</p>;
    }



    return (
        <div className="form-personal-info">
            <form onSubmit={formik.handleSubmit} className="form">
                <div className="container conatiner-personal-info">
                    <div className="row input-container">
                        <h2 className="col-lg-12 col-md-12 col-12 patient-information">
                            Información Paciente
                        </h2>
                        
                        {/* Nombre */}
                        <div className="col-lg-6 col-md-6 col-12">
                            <div className="form-group form-group-info">
                                <p><strong><label htmlFor="name">Nombre:</label></strong></p>
                                <input
                                    name="name"
                                    type="text"
                                    onChange={formik.handleChange}
                                    onBlur={formik.handleBlur}
                                    value={formik.values.name}
                                    className={formik.touched.name && formik.errors.name ? "error-input" : ""}
                                />
                                {formik.touched.name && formik.errors.name && (
                                    <p className="error">{formik.errors.name}</p>
                                )}
                            </div>
                        </div>

                        {/* Apellido */}
                        <div className="col-lg-6 col-md-6 col-12">
                            <div className="form-group form-group-info">
                                <p><strong><label htmlFor="last_name">Apellido:</label></strong></p>
                                <input
                                    name="last_name"
                                    type="text"
                                    onChange={formik.handleChange}
                                    onBlur={formik.handleBlur}
                                    value={formik.values.last_name}
                                    className={formik.touched.last_name && formik.errors.last_name ? "error-input" : ""}
                                />
                                {formik.touched.last_name && formik.errors.last_name && (
                                    <p className="error">{formik.errors.last_name}</p>
                                )}
                            </div>
                        </div>

                        {/* Fecha de Nacimiento */}
                        <div className="col-lg-5 col-md-6 col-12">
                            <div className="form-group form-group-info-birthday">
                                <p><strong><label htmlFor="birthday">Fecha de Nacimiento:</label></strong></p>
                                <input
                                    name="birthday"
                                    type="date"
                                    onChange={formik.handleChange}
                                    onBlur={formik.handleBlur}
                                    value={formik.values.birthday}
                                    max={new Date().toISOString().split('T')[0]}
                                    className={formik.touched.birthday && formik.errors.birthday ? "error-input" : ""}
                                />
                                {formik.touched.birthday && formik.errors.birthday && (
                                    <p className="error">{formik.errors.birthday}</p>
                                )}
                            </div>
                        </div>

                        {/* Email */}
                        <div className="col-lg-7 col-md-6 col-12">
                            <div className="form-group form-group-info-email">
                                <p><strong><label htmlFor="email">Email:</label></strong></p>
                                <input
                                    name="email"
                                    type="email"
                                    onChange={formik.handleChange}
                                    onBlur={formik.handleBlur}
                                    value={formik.values.email}
                                    className={formik.touched.email && formik.errors.email ? "error-input" : ""}
                                />
                                {formik.touched.email && formik.errors.email && (
                                    <p className="error">{formik.errors.email}</p>
                                )}
                            </div>
                        </div>

                        {/* Whatsapp */}
                        <div className="col-lg-6 col-md-6 col-12">
                            <div className="form-group form-group-info">
                                <p><strong><label htmlFor="whatsapp">Whatsapp:</label></strong></p>
                                <input
                                    name="whatsapp"
                                    type="text"
                                    onChange={formik.handleChange}
                                    onBlur={formik.handleBlur}
                                    value={formik.values.whatsapp}
                                    placeholder="Ej: +51987654321"
                                    className={formik.touched.whatsapp && formik.errors.whatsapp ? "error-input" : ""}
                                />
                                {formik.touched.whatsapp && formik.errors.whatsapp && (
                                    <p className="error">{formik.errors.whatsapp}</p>
                                )}
                            </div>
                        </div>

                        {/* País */}
                        <div className="col-lg-6 col-md-6 col-12">
                            <div className="form-group">
                                <p><strong><label htmlFor="country">País:</label></strong></p>
                                <select
                                    name="country"
                                    onChange={formik.handleChange}
                                    onBlur={formik.handleBlur}
                                    value={formik.values.country}
                                    className={formik.touched.country && formik.errors.country ? "error-input" : ""}
                                >
                                    <option value="">-- Selecciona un país --</option>
                                    {countries.map((country, index) => (
                                        <option key={`${country.country}-${index}`} value={country.country}>
                                            {country.country}
                                        </option>
                                    ))}
                                </select>
                                {formik.touched.country && formik.errors.country && (
                                    <p className="error">{formik.errors.country}</p>
                                )}
                            </div>
                        </div>

                        {/* Ciudad */}
                        <div className="col-lg-6 col-md-6 col-12">
                            <div className="form-group">
                                <p><strong><label htmlFor="city">Ciudad:</label></strong></p>
                                <select
                                    name="city"
                                    onChange={formik.handleChange}
                                    onBlur={formik.handleBlur}
                                    value={formik.values.city}
                                    disabled={!formik.values.country || loadingStates.cities}
                                    className={formik.touched.city && formik.errors.city ? "error-input" : ""}
                                >
                                    <option value="">-- Selecciona una ciudad --</option>
                                    {cities.map((city, index) => (
                                        <option key={`${city}-${index}`} value={city}>
                                            {city}
                                        </option>
                                    ))}
                                </select>
                                {loadingStates.cities && formik.values.country && (
                                    <p className="loading-text">Cargando ciudades...</p>
                                )}
                                {formik.touched.city && formik.errors.city && (
                                    <p className="error">{formik.errors.city}</p>
                                )}
                            </div>
                        </div>

                        {/* Sexo */}
                        <div className="col-lg-6 col-md-6 col-12">
                            <div className="form-group form-group-info">
                                <p><strong><label htmlFor="sex">Sexo:</label></strong></p>
                                <select
                                    name="sex"
                                    onChange={formik.handleChange}
                                    onBlur={formik.handleBlur}
                                    value={formik.values.sex}
                                    className={formik.touched.sex && formik.errors.sex ? "error-input" : ""}
                                >
                                    <option value="">-- Seleccione --</option>
                                    <option value="Masculino">Masculino</option>
                                    <option value="Femenino">Femenino</option>
                                   
                                </select>
                                {formik.touched.sex && formik.errors.sex && (
                                    <p className="error">{formik.errors.sex}</p>
                                )}
                            </div>
                        </div>

                        {/* Peso */}
                        <div className="col-lg-6 col-md-6 col-12">
                            <div className="form-group form-group-info">
                                <p><strong><label htmlFor="weight">Peso (lb):</label></strong></p>
                                <input
                                    name="weight"
                                    type="number"
                                    onChange={formik.handleChange}
                                    onBlur={formik.handleBlur}
                                    value={formik.values.weight}
                                    min="20"
                                    max="300"
                                    className={formik.touched.weight && formik.errors.weight ? "error-input" : ""}
                                />
                                {formik.touched.weight && formik.errors.weight && (
                                    <p className="error">{formik.errors.weight}</p>
                                )}
                            </div>
                        </div>

                        {/* Estatura */}
                        <div className="col-lg-6 col-md-6 col-12">
                            <div className="form-group form-group-info">
                                <p><strong><label htmlFor="height">Estatura (cm):</label></strong></p>
                                <input
                                    name="height"
                                    type="number"
                                    onChange={formik.handleChange}
                                    onBlur={formik.handleBlur}
                                    value={formik.values.height}
                                    min="50"
                                    max="250"
                                    className={formik.touched.height && formik.errors.height ? "error-input" : ""}
                                />
                                {formik.touched.height && formik.errors.height && (
                                    <p className="error">{formik.errors.height}</p>
                                )}
                            </div>
                        </div>

                        {/* Objetive */}
                        <div className="col-lg-6 col-md-6 col-12">
                            <div className="form-group form-group-info">
                                <p><strong><label htmlFor="sex">Objetivo:</label></strong></p>
                                <select
                                    name="objetive"
                                    onChange={formik.handleChange}
                                    onBlur={formik.handleBlur}
                                    value={formik.values.objetive}
                                    className={formik.touched.objetive && formik.errors.objetive ? "error-input" : ""}
                                >
                                    <option value="">-- Seleccione --</option>
                                    <option value="Bajar de peso">Bajar de Peso</option>
                                    <option value="Subir de peso">Subir de peso</option>
                                   
                                </select>
                                {formik.touched.objetive && formik.errors.objetive && (
                                    <p className="error">{formik.errors.objetive}</p>
                                )}
                            </div>
                        </div>

                        {/* Alergias */}
                        <div className="col-lg-12 col-md-6 col-12">
                            <div className="form-group form-group-info-textarea">
                                <p><strong><label htmlFor="food_allergies">Alimentos que no consume o es alérgico:</label></strong></p>
                                <textarea
                                    className={`form-control ${formik.touched.food_allergies && formik.errors.food_allergies ? "error-input" : ""}`}
                                    name="food_allergies"
                                    onChange={formik.handleChange}
                                    onBlur={formik.handleBlur}
                                    value={formik.values.food_allergies}
                                    rows="4"
                                    maxLength="500"
                                ></textarea>
                                {formik.touched.food_allergies && formik.errors.food_allergies && (
                                    <p className="error">{formik.errors.food_allergies}</p>
                                )}
                            </div>
                        </div>

                        {/* Enfermedades */}
                        <div className="col-lg-12 col-md-6 col-12">
                            <div className="form-group form-group-info-textarea">
                                <p><strong><label htmlFor="diseases">Enfermedades o Lesiones que padece:</label></strong></p>
                                <textarea
                                    className={`form-control ${formik.touched.diseases && formik.errors.diseases ? "error-input" : ""}`}
                                    name="diseases"
                                    onChange={formik.handleChange}
                                    onBlur={formik.handleBlur}
                                    value={formik.values.diseases}
                                    rows="4"
                                    maxLength="500"
                                ></textarea>
                                {formik.touched.diseases && formik.errors.diseases && (
                                    <p className="error">{formik.errors.diseases}</p>
                                )}
                            </div>
                            <input type="hidden" name="doctor" value={formik.values.doctor} />
                        </div>

                        {/* CAPTCHA */}
                        <div className="col-lg-12 col-md-12 col-12">
                            <div className="form-group">
                                <ReCAPTCHA
                                    sitekey={RECAPTCHA_SITE_KEY}
                                    onChange={handleCaptchaChange}
                                />
                                {formik.touched.captcha && formik.errors.captcha && (
                                    <p className="error">{formik.errors.captcha}</p>
                                )}
                            </div>
                        </div>

                        {/* Mensajes */}
                        {message && (
                            <div className={`col-12 alert ${message.type === "success" ? "alert-success" : "alert-danger"}`}>
                                {message.text}
                            </div>
                        )}

                        {/* Botón de envío */}
                        <div className="col-lg-12 col-md-12 col-12">
                            <button
                                type="submit"
                                className="btn btn-primary"
                                disabled={isSubmitting || !formik.isValid}
                            >
                                {isSubmitting ? (
                                    <>
                                        <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                                        <span className="ml-2">Enviando...</span>
                                    </>
                                ) : (
                                    "Enviar Formulario"
                                )}
                            </button>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    );
};

export default PersonalInformationForm;