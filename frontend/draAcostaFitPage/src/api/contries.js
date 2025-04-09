
/*import axios from 'axios';

const API_CONTRIES_URL = 'https://countriesnow.space/api/v0.1/countries'

const apiCountries = axios.create({
    baseURL: API_CONTRIES_URL, 
    headers: {
        'Content-Type': 'application/json',
    }
});



//Get Countries
export const getCountries = async () => {
    try{
        const response = await apiCountries.get('/');
        return response.data.data; // return only the coutries
      }catch(error){
        console.error('Error to fetching countries data');
        throw error;
      }
};


export const getCitiesByCountry = async (country) =>{
    try{
        const response = await apiCountries.post('/cities', {country})
        return response.data.data; // retunr de cities
     }catch (error){
        console.error('Error al obtener ciudades:', error);
        throw error;
     }
};*/


import axios from 'axios';

const API_CONTRIES_URL = 'https://countriesnow.space/api/v0.1/countries';

const apiCountries = axios.create({
    baseURL: API_CONTRIES_URL,
    headers: { 'Content-Type': 'application/json' },
});

// Obtener países
export const getCountries = async () => {
    try {
        const response = await apiCountries.get('');
        return response.data.data; // Solo devuelve los países
    } catch (error) {
        console.error('Error al obtener países:', error);
        return [];
    }
};

// Obtener ciudades por país
export const getCitiesByCountry = async (country) => {
    try {
        const response = await apiCountries.post('/cities', { country });
        return response.data.data; // Solo devuelve las ciudades
    } catch (error) {
        console.error(`Error al obtener ciudades para ${country}:`, error);
        return [];
    }
};
 