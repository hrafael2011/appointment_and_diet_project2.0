/*
import axios from 'axios'

const apiClient = axios.create({
    baseURL : 'http://localhost:8000/api/'
});

// Interceptores para manejar errores globalmente

// Interceptores para manejar errores globalmente
apiClient.interceptors.response.use(
    response => response,
    error => {
        console.error('API Error:', error.response || error.message);
        return Promise.reject(error);
    }
);

export default apiClient;*/

import axios from 'axios';

const API_BASE_URL = "http://localhost:8000/api/"; // 🔥 Corregido

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        "Content-Type": "application/json",
    }
});

export const postAppointment = async (appointmentData) => { // 🔥 Debe recibir datos
    console.log("Enviando datos:", appointmentData);
    try {
        const response = await api.post('appointment/', appointmentData); // 🔥 Agregado /
        return response.data;
    } catch (error) {
        console.error('Error al enviar la cita:', error);
        throw error;
    }
};

export const validateCancellation = async(token) =>{
    try{
        const response = await api.get(`appointment/validate-cancellation/?token=${token}`)
        return response.data //Retorna los datos nesesarios como este case patient_name
      }catch(error){
        console.error('Error al validar Token', error)
        throw error.response?.error || "Error al validar token";
      }
};

export const cancelAppointment = async(token) =>{
    if (!token) {
        throw new Error('El token es requerido');
    }
    try{
        const response = await api.post('appointment/cancel/',{token});
       
        return response.data; // Retorna los mensajes del backend
    }catch(error){
        console.error('Error al cancelar cita:', error)
        throw error.response?.data?.error || "Error al cancelar la cita";
    }
};


export const getAvailableHours = async(date) =>{
    try{
        //const response = await api.get(`doctor/available/?date=${date}`)
        const response = await api.get(`doctor/available/`, {
            params: { date: date }, // Pasar la fecha como un parámetro de consulta
        });
        console.log('Horas se cargan', response)
    return response.data;

    }catch(error){
        console.error('Error al obtener la disponbilidad')
        throw error;
    }
    
};

