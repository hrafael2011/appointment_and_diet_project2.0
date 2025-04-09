import React from 'react'
import AppointmentForm from './AppointmentForm '

export const MakeAppointment = () => {
  return (
    <>
    {/*<!-- Start Appointment -->*/}
		<section className="appointment">
			<div className="container">
				<div className="row">
					<div className="col-lg-12">
						<div className="section-title">
							<h2>We Are Always Ready to Help You. Book An Appointment</h2>
							<img src="img/section-img.png" alt="#"/>
							<p>Lorem ipsum dolor sit amet consectetur adipiscing elit praesent aliquet. pretiumts</p>
						</div>
					</div>
				</div>
				<div className="row">
					<div className="col-lg-6 col-md-12 col-12">
				
					<AppointmentForm/>
					</div>
					<div className="col-lg-6 col-md-12 ">
						<div className="appointment-image">
							<img src="https://via.placeholder.com/520x520" alt="#"/>
						</div>
					</div>
				</div>
			</div>
		</section>
		{/*<!-- End Appointment -->*/}
    
    </>
  )
}
