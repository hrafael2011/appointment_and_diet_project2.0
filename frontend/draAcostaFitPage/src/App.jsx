import { useState } from 'react'
import { Header } from './components/Header'
import Slider from './components/Slider'
import { IntroductionService } from './components/IntroductionService'
import { BeforeAndAfter } from './components/BeforeAndAfter'
import { CounterServices } from './components/CounterServices'
import WhoWeAre from './components/WhoWeAre'
import { Services } from './components/Services'
import { PatietTestimonial } from './components/PatietTestimonial'
import { PlansPrice } from './components/PlansPrice'
import { MakeAppointment } from './components/MakeAppointment'
import { Suscribe } from './components/Suscribe'
import { Footer } from './components/Footer'
import { Preloader } from './components/Preloader'
import { ColorPlate } from './components/ColorPlate'
import { Routers } from './routes/Routers'

function App() {
  
  return (
    <>
   <Routers/>
    <ColorPlate/>
    

      
    </>
  )
}

export default App
