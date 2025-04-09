import React from 'react'

export const Header = () => {
  return (
    <>
    {/*<!-- Header Area -->*/}
		<header className="header">
			{/*<!-- Topbar -->*/}
			<div className="topbar">
				<div className="container">
					<div className="row">
						<div className="col-lg-6 col-md-5 col-12">
							{/*<!-- Contact -->*/}
							<ul className="top-link">
								<li><a href="#">About</a></li>
								<li><a href="#">Doctors</a></li>
								<li><a href="#">Contact</a></li>
								<li><a href="#">FAQ</a></li>
							</ul>
							{/*<!-- End Contact -->*/}
						</div>
						<div className="col-lg-6 col-md-7 col-12">
							{/*<!-- Top Contact -->*/}
							<ul className="top-contact">
								<li><i className="fa fa-phone"></i>+880 1234 56789</li>
								<li><i className="fa fa-envelope"></i><a href="mailto:support@yourmail.com">support@yourmail.com</a></li>
							</ul>
							{/*<!-- End Top Contact -->*/}
						</div>
					</div>
				</div>
			</div>
			{/*<!-- End Topbar -->*/}
			{/*<!-- Header Inner -->*/}
			<div className="header-inner">
				<div className="container">
					<div className="inner">
						<div className="row">
							<div className="col-lg-3 col-md-3 col-12">
								{/*<!-- Start Logo -->*/}
								<div className="logo">
									<a href="index.html"><img src="img/logo.png" alt="#"/></a>
								</div>
								{/*<!-- End Logo -->*/}
								{/*<!-- Mobile Nav -->*/}
								<div className="mobile-nav"></div>
								{/*<!-- End Mobile Nav -->*/}
							</div>
							<div className="col-lg-7 col-md-9 col-12">
								{/*<!-- Main Menu -->*/}
								<div className="main-menu">
									<nav className="navigation">
										<ul className="nav menu">
											<li className="active"><a href="#">Home <i className="icofont-rounded-down"></i></a>
												<ul className="dropdown">
													<li><a href="index.html">Home Page 1</a></li>
													<li><a href="index2.html">Home Page 2</a></li>
												</ul>
											</li>
											<li><a href="#">Doctos <i className="icofont-rounded-down"></i></a>
												<ul className="dropdown">
													<li><a href="doctors.html">Doctor</a></li>
													<li><a href="doctor-details.html">Doctor Details</a></li>
												</ul>
											</li>
											<li><a href="#">Services <i className="icofont-rounded-down"></i></a>
												<ul className="dropdown">
													<li><a href="service.html">Service</a></li>
													<li><a href="service-details.html">Service Details</a></li>
												</ul>
											</li>
											<li><a href="#">Pages <i className="icofont-rounded-down"></i></a>
												<ul className="dropdown">
													<li><a href="about.html">About Us</a></li>
													<li><a href="appointment.html">Appointment</a></li>
													<li><a href="time-table.html">Time Table</a></li>
													<li><a href="testimonials.html">Testimonials</a></li>
													<li><a href="pricing.html">Our Pricing</a></li>
													<li><a href="register.html">Sign Up</a></li>
													<li><a href="login.html">Login</a></li>
													<li><a href="faq.html">Faq</a></li>
													<li><a href="mail-success.html">Mail Success</a></li>
													<li><a href="404.html">404 Error</a></li>
												</ul>
											</li>
											<li><a href="#">Blogs <i className="icofont-rounded-down"></i></a>
												<ul className="dropdown">
													<li><a href="blog-grid.html">Blog Grid</a></li>
													<li><a href="blog-single.html">Blog Details</a></li>
												</ul>
											</li>
											<li><a href="contact.html">Contact Us</a></li>
										</ul>
									</nav>
								</div>
								{/*<!--/ End Main Menu -->*/}
							</div>
							<div className="col-lg-2 col-12">
								<div className="get-quote">
									<a href="appointment.html" className="btn">Book Appointment</a>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
			{/*{/*<!--/ End Header Inner -->*/}
		</header>
    </>
  )
}
