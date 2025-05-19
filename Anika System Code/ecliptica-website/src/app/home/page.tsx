import Image from "next/image";
import Head from "next/head";
import Link from "next/link";
import { Check } from "lucide-react";
import { Button } from "@/components/ui/button";
import Slider from "@/components/ui/Slider";

export default function Home() {
	return (
		// Title Section
		<div className="overflow-x-hidden">
			<Head>
				<title>Innovative Technology. Empowering Research.</title>
				<meta
					name="description"
					content="Ecliptica: Built for your research experience, simplified by AI."
				/>
			</Head>
			<div className="min-h-screen flex items-center justify-center bg-white">
				<div className="flex lg:flex-row lg:items-start w-full">
					<div className="lg:w-1/2 space-y-6 m-auto px-20">
						<h1 className="text-6xl text-center text-[#005eb4] leading-tight tracking-wider font-bold">
							Innovative Technology. <br />
							Empowering Research.
						</h1>
						<p className="text-center text-2xl text-gray-800 tracking-wider w-3/4 left-10 relative">
							Meet{" "}
							<span id="what-do-we-do" className="font-bold text-[#007698]">
								Ecliptica
							</span>
							. Built for your research experience, simplified
							by{" "}
							<span className="font-bold text-[#007698]">AI</span>
							.
						</p>
						<Link href="#what-do-we-do" >
							<button className="text-center items-center justify-center left-20 relative bg-[#007698] text-white py-4 px-10 rounded-full text-lg font-medium mt-4 hover:bg-blue-700 transition">
								Learn about us &rarr;
							</button>
						</Link>
					</div>

					<div
						className="mt-10 left-7 relative w-[100vw] h-[105vh] bg-cover bg-center"
						style={{ backgroundImage: "url(/imgs/home_logo.svg)" }}
					/>
				</div>
			</div>

			{/* Information Section */}
			<div className="bg-[#d4ecff] w-full">
			<div className="flex flex-col items-center justify-center relative space-y-8 py-20">
				<p className="text-[#005eb4] text-5xl tracking-wider">
				What Do We Do?
				</p>
				<p className="text-2xl w-4/5 text-center mx-8">
				Our mission at Ecliptica is to harness the 
				<span className="font-bold text-[#007698]"> power of AI</span> to make research processes more 
				<span className="font-bold text-[#007698]"> accessible</span>, 
				<span className="font-bold text-[#007698]"> personalized</span>, and 
				<span className="font-bold text-[#007698]"> efficient</span> for everyone. By combining cutting-edge 
				technology with compassionate care, we aim to empower individuals to 
				<span className="font-bold text-[#007698]"> take control of their research journeys</span>, leading to better outcomes and lives. 
				Input a word into our website, and find a list of reputable publications that support your keyword, 
				along with a compilation of many data visualizations that illustrate the publication's information 
				concisely!
				</p>
			</div>
			</div>

			{/* Ready-to-manage-your-research section */}
			<div className="bg-white w-full relative bottom-12 mt-20">
			<div className="flex justify-center items-center flex-col space-y-5">
				<h1 className="text-center text-5xl tracking-wider text-[#005eb4] leading-relaxed">
				Ready to manage your research <br />
				<span>with just one word?</span>
				</h1>

				<p className="mt-5 text-2xl tracking-wide w-full text-center">
				Use our research model and{" "}
				<span className="font-black text-[#007698]">
					eclipse
				</span>{" "}
				the research world with ease.{" "}
				</p>

				<Link
				href="/about#what-do-you-want-to-research">
					<button className="text-center items-center justify-center center-20 relative bg-[#007698] text-white py-4 px-10 rounded-full text-lg font-medium mt-4 hover:bg-blue-700 transition">
						Use Ecliptica Now &rarr;
					</button>
				</Link>
			</div>
			</div>

			{/* Slider */}
			<div className="flex justify-center items-center w-full mt-8 mb-12">
			<div className="w-4/5 md:w-3/4 lg:w-2/3">
				<Slider />
			</div>
			</div>

			{/* Checkpoints section */}
			<div className="relative mb-0 mt-0 flex w-full bg-[#d4ecff] py-16">
			<div className="flex justify-center items-center w-1/2">
				<img
				src="/imgs/data-guy.jpg"
				className="object-cover z-10 w-[90%] sm:w-[80%] md:w-[75%] lg:w-[70%] h-auto"
				alt="Chatbot illustration"
				/>
			</div>

			{/* Ending-of-home-page section */}
			<div className="flex flex-col justify-center items-center w-1/2 space-y-8">
				<CheckList text="Eliminate the stress of researching hours upon hours" />
				<CheckList text="Get AI recommendations and research analysis" />
				<CheckList text="Upload datasets and access specialized data visualizations" />
			</div>
			</div>
			<div className="bg-[#99ceff] w-full h-72 items-center justify-center flex flex-col">
				<div className="space-y-10">
					<p className="text-5xl text-[#005eb4]">Research With Ease</p>
					<p className="text-xl tracking-wider text-[#005eb4] text-center relative">
						Start your independent research journey.
					</p>
				</div>

				<Link
					href="/about#possible-data-visualizations">
					<button className="text-center items-center justify-center center-20 relative bg-[#007698] text-white py-4 px-10 rounded-full text-lg font-medium mt-4 hover:bg-blue-700 transition">
								Explore Ecliptica &rarr;
					</button>
				</Link>
			</div>
		</div>
	);
}

// Checklist section
interface CheckListProps {
	text: string;
  }
  
  const CheckList = ({ text }: CheckListProps) => {
	return (
	  <div className="flex flex-row items-start space-x-12 w-full max-w-2xl">
		<Check className="h-6 w-6 text-[#007698]" />
		<p className="tracking-widest text-2xl flex-grow mr-12 break-words">
		  {text}
		</p>
	  </div>
	);
  };