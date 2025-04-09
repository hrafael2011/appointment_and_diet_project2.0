

import { useState, useEffect } from "react"; // Importamos useEffect
import { useFormik } from "formik";
import * as Yup from "yup";
import ReCAPTCHA from "react-google-recaptcha";
import { postAppointment, getAvailableHours } from "../api/apiClients";

const doctorId = 1;

const AppointmentForm = () => {
    const [message, setMessage] = useState(null); // Estado para manejar mensajes
    const [hourAvailable, setHourAvailable] = useState([]); // Almacena horarios disponibles
    const [isLoading, setIsLoading] = useState(false); // Indicador de carga

    const formik = useFormik({
        initialValues: {
            name: "",
            last_name: "",
            email: "",
            whatsapp: "",
            date: "",
            hour: "",
            doctor: doctorId,
            captcha: "", // Nuevo campo para el CAPTCHA
        },
        validationSchema: Yup.object({
            name: Yup.string().required("El nombre es obligatorio"),
            last_name: Yup.string().required("El apellido es obligatorio"),
            email: Yup.string()
                .email("Correo electrónico no válido")
                .required("El correo electrónico es obligatorio"),
            whatsapp: Yup.string()
                .matches(/^\+?[0-9]{10,15}$/, "Número de teléfono no válido")
                .required("El número de teléfono es obligatorio"),
            date: Yup.string().required("La fecha es obligatoria"),
            hour: Yup.string().required("La hora es obligatoria"),
            captcha: Yup.string().required("Por favor, completa el CAPTCHA."),
        }),
        onSubmit: async (values, { resetForm }) => {
            try {
                console.log("Enviando datos...", values); // Depuración
                const response = await postAppointment(values);
                console.log("Cita creada:", response);

                // Mostrar mensaje de éxito
                setMessage({
                    type: "success",
                    text: "Se ha enviado un correo electrónico de confirmación. Por favor, revise su bandeja de entrada y siga las instrucciones para confirmar su cita.",
                });

                resetForm();
            } catch (error) {
                console.error("Error:", error); // Depuración

                // Mostrar mensaje de error
                setMessage({
                    type: "error",
                    text: "Hubo un error al procesar su solicitud. Por favor, inténtelo de nuevo más tarde.",
                });
            }
        },
    });

    // useEffect para cargar horarios disponibles cuando cambie la fecha
    useEffect(() => {
        const fetchAvailableHours = async () => {
            if (formik.values.date) {
                console.log("Cargando horarios para la fecha:", formik.values.date);
                setHourAvailable([]); // Limpia horarios previos
                setIsLoading(true); // Inicia el estado de carga

                try {
                    const schedule = await getAvailableHours(formik.values.date);
                    console.log("Horarios disponibles recibidos:", schedule);
                    setHourAvailable(schedule);
                } catch (error) {
                    console.error("Error al cargar horarios:", error);
                    setHourAvailable([]); // Reinicia el estado si ocurre error
                } finally {
                    setIsLoading(false); // Finaliza el estado de carga
                }
            }
        };

        fetchAvailableHours(); // Llama a la función cuando cambie la fecha
    }, [formik.values.date]); // Se ejecuta cada vez que cambie la fecha seleccionada

    // Función para manejar el cambio del CAPTCHA
    const handleCaptchaChange = (value) => {
        formik.setFieldValue("captcha", value); // Actualiza el valor del CAPTCHA en Formik
    };

    return (
        <form onSubmit={formik.handleSubmit} className="form">
            <div className="row">
                {/* Campos de entrada para la cita */}
                <div className="col-lg-6 col-md-6 col-12">
                    <div className="form-group">
                        <input
                            name="name"
                            type="text"
                            placeholder="Nombre"
                            onChange={formik.handleChange}
                            onBlur={formik.handleBlur}
                            value={formik.values.name}
                        />
                        {formik.touched.name && formik.errors.name && (
                            <p className="error">{formik.errors.name}</p>
                        )}
                    </div>
                </div>

                <div className="col-lg-6 col-md-6 col-12">
                    <div className="form-group">
                        <input
                            name="last_name"
                            type="text"
                            placeholder="Apellido"
                            onChange={formik.handleChange}
                            onBlur={formik.handleBlur}
                            value={formik.values.last_name}
                        />
                        {formik.touched.last_name && formik.errors.last_name && (
                            <p className="error">{formik.errors.last_name}</p>
                        )}
                    </div>
                </div>

                <div className="col-lg-6 col-md-6 col-12">
                    <div className="form-group">
                        <input
                            name="email"
                            type="email"
                            placeholder="Correo electrónico"
                            onChange={formik.handleChange}
                            onBlur={formik.handleBlur}
                            value={formik.values.email}
                        />
                        {formik.touched.email && formik.errors.email && (
                            <p className="error">{formik.errors.email}</p>
                        )}
                    </div>
                </div>

                <div className="col-lg-6 col-md-6 col-12">
                    <div className="form-group">
                        <input
                            name="whatsapp"
                            type="text"
                            placeholder="WhatsApp (ej: +1234567890)"
                            onChange={formik.handleChange}
                            onBlur={formik.handleBlur}
                            value={formik.values.whatsapp}
                        />
                        {formik.touched.whatsapp && formik.errors.whatsapp && (
                            <p className="error">{formik.errors.whatsapp}</p>
                        )}
                    </div>
                </div>

                {/* Fecha de la cita */}
                <div className="col-lg-6 col-md-6 col-12">
                    <div className="form-group">
                        <input
                            name="date"
                            type="date"
                            onChange={formik.handleChange} // Ahora solo manejamos Formik
                            onBlur={formik.handleBlur}
                            value={formik.values.date}
                        />
                        {formik.touched.date && formik.errors.date && (
                            <p className="error">{formik.errors.date}</p>
                        )}
                    </div>
                </div>

                {/* Hora de la cita */}
                <div className="col-lg-6 col-md-6 col-12">
                    <div className="form-group">
                        {isLoading ? (
                            <p>Cargando horarios disponibles...</p>
                        ) : (
                            <select
                                name="hour"
                                onChange={formik.handleChange}
                                onBlur={formik.handleBlur}
                                value={formik.values.hour}
                                disabled={hourAvailable.length === 0} // Desactiva si no hay horarios
                            >
                                <option value="">Selecciona una Hora</option>
                                {hourAvailable.map((hours, index) => (
                                    <option key={index} value={hours.hour}>
                                        {hours.hour}
                                    </option>
                                ))}
                            </select>
                        )}

                        {formik.touched.hour && formik.errors.hour && (
                            <p className="error">{formik.errors.hour}</p>
                        )}
                    </div>
                </div>

                <input type="hidden" name="doctor" value={formik.values.doctor} />
            </div>

            {/* CAPTCHA */}
            <div className="form-group">
                <ReCAPTCHA
                    sitekey="6LdYHOsqAAAAAFbDkivAKIBuZUF4cvSnt_whB2U5"
                    onChange={handleCaptchaChange}
                />
                {formik.touched.captcha && formik.errors.captcha && (
                    <p className="error">{formik.errors.captcha}</p>
                )}
            </div>

            {/* Mensaje de éxito o error */}
            {message && (
                <div
                    className={`message ${
                        message.type === "success" ? "success" : "error"
                    }`}
                >
                    {message.text}
                </div>
            )}

            <button type="submit" className="btn" disabled={formik.isSubmitting}>
                Reservar Cita
            </button>
        </form>
    );
};

export default AppointmentForm;

