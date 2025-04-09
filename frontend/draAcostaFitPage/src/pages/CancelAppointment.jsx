
import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { validateCancellation, cancelAppointment } from '../api/apiClients';

export const CancelAppointment = () => {
  const navigate = useNavigate(); // Cambiado el nombre para reflejar correctamente el hook actual
  const query = new URLSearchParams(useLocation().search);
  const token = query.get('token');
  console.log('Token Capturado', token)

  const [patientName, setPatientName] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    // Validar el token utilizando la función de la API
    if (!token) {
      setError('Token no proporcionado.'); // Manejar la falta de token
      return;
    }

    validateCancellation(token)
      .then((data) => {
        setPatientName(data.patient_name);
      })
      .catch((errorMessage) => {
        setError(errorMessage);
      });
  }, [token]);

  const handleCancel = () => {
    if (!token) {
      alert('No se puede cancelar la cita sin un token válido.');
      return;
    }

    cancelAppointment(token)
      .then((data) => {
        alert(data.message);
        navigate('/'); // Redirigir al inicio después de cancelar
      })
      .catch((errorMessage) => {
        alert(errorMessage);
        //navigate('/'); // Redirigir incluso si hay un error
      });
  };

  const handleNoCancel = () => {
    navigate('/'); // Regresar al inicio si decide no cancelar
  };

  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  return (
    <>
      <div>
        <h1>Cancelar Cita</h1>
        <p>Señor {patientName}, ¿está seguro que desea cancelar su cita?</p>
        <button onClick={handleCancel}>Sí, cancelar</button>
        <button onClick={handleNoCancel}>No, conservar cita</button>
      </div>
    </>
  );
};
