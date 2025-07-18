import React from 'react'
import {BrowserRouter, Routes, Route} from 'react-router-dom'
import { Layout } from '../components/Layout'

import { CancelAppointment } from '../pages/CancelAppointment'
import {ConfirmAppointment} from "../pages/ConfirmAppointment"
import { Home } from '../pages/Home'
import PersonalIformationForm from '../components/PersonalIformationForm '

export const Routers = () => {
  return (
    <BrowserRouter>
        <Routes >
          <Route path="/" element={<Layout />}>
            <Route index element={<Home/>}/>
            <Route path="cancelacion-cita" element={<CancelAppointment />} />
            <Route path="confirmacion-cita" element={<ConfirmAppointment />} />
            
          </Route>
          <Route path='/informacion-personal-form/:id' element={<PersonalIformationForm/>} />
        </Routes>
    </BrowserRouter>
  )
}
