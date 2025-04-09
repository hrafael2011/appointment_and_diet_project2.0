import React from 'react';
import Slider from '../components/Slider';
import { IntroductionService } from '../components/IntroductionService';
import { BeforeAndAfter } from '../components/BeforeAndAfter';
import { CounterServices } from '../components/CounterServices';
import WhoWeAre from '../components/WhoWeAre';
import { Services } from '../components/Services';
import { PatietTestimonial } from '../components/PatietTestimonial';
import { PlansPrice } from '../components/PlansPrice';
import { MakeAppointment } from '../components/MakeAppointment';
import { Suscribe } from '../components/Suscribe';

export const Home = () => {
  return (
    <>
      <Slider />
      <IntroductionService />
      <BeforeAndAfter />
      <CounterServices />
      <WhoWeAre />
      <Services />
      <PatietTestimonial />
      <PlansPrice />
      <MakeAppointment />
      <Suscribe />
    </>
  );
};
