

import axios from 'axios';

const API_BASE_URL = "http://localhost:8000/api/"; // 🔥 Corregido

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        "Content-Type": "application/json",
    }
});


export const getPatientById = async (id) => {
    try {
        const response = await api.get(`patient/${id}/`); // 🔥 ID dinámico en el endpoint
        return response.data; // Devuelve los datos del paciente específico
    } catch (error) {
        console.error(`Error al obtener el paciente con ID ${id}:`, error);
        throw error; // Manejo del error
    }
};


export const putPatient = async (id, patientData) => { // Recibe el id del paciente y los datos a actualizar
    console.log("Actualizando datos del paciente:", patientData);
    try {
        const response = await api.put(`patient/${id}/`, patientData); // Se usa PUT y la URL incluye el id dinámico
        return response.data;
    } catch (error) {
        console.error('Error al actualizar datos del paciente:', error);
        throw error;
    }
};