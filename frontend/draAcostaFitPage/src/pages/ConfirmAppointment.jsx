/*import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { confirmAppointment } from '../api/apiClients';

export const ConfirmAppointment = () => {
  const query = new URLSearchParams(useLocation().search);
  const token = query.get('token');
  console.log('Token Capturado', token)

  const [patientName, setPatientName] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    if (!token) {
      setError('Token no proporcionado');
      return;
    }

    confirmAppointment(token)
      .then(data => {
        setPatientName(data.patient_name);
        setMessage(data.message || 'Cita confirmada exitosamente');
      })
      .catch(err => {
        setError(err);
      });
  }, [token]);

  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <>
      <h1>Cita Confirmada</h1>
      <p>{patientName}, {message}</p>
    </>
  );
};*/

import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { confirmAppointment } from '../api/apiClients';

export const ConfirmAppointment = () => {
  const query = new URLSearchParams(useLocation().search);
  const token = query.get('token');

  const [patientName, setPatientName] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true); // Estado para controlar la carga

  useEffect(() => {
    if (!token) {
      setError('Token no proporcionado');
      setLoading(false);
      return;
    }

    confirmAppointment(token)
      .then(data => {
        console.log('Respuesta del backend:', data);
        setPatientName(data.patient_name);
        setMessage(data.message || 'Cita confirmada exitosamente');
      })
      .catch(err => {
        setError('Error al confirmar la cita');
      })
      .finally(() => {
        setLoading(false);
      });
  }, [token]);

  if (loading) return <p>Cargando confirmación...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <>
      <h1>Cita Confirmada</h1>
      <p>{patientName}, {message}</p>
    </>
  );
};
