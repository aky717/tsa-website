import Image from "next/image";

export default function DataVisualizations() {
  // Different-types-of-visualizations
  const visualizations = [
    { src: "/imgs/new-piechart.jpg", alt: "Pie Charts", description: "Pie Chart: Shows a visual of how the inputted topic is distributed by percent throughout related topics.", bgColor: "#007698" },
    { src: "/imgs/new-bargraph.jpg", alt: "Bar Graph", description: "Bar Graph: Uses the given topic and displays the number of publications for each subtopic.", bgColor: "#035db4" },
    { src: "/imgs/new-linechart.jpg", alt: "Line Charts", description: "Line Chart: Input a topic and display a trend of the topic over the years.", bgColor: "#99ceff" },
    { src: "/imgs/new-sunburstchart.jpg", alt: "Sunburst Charts", description: "Sunburst Chart: Shows a visual of all the keywords related to each of the subtopics within the topic selected.", bgColor: "#035db4" },
    { src: "/imgs/new-scatterplotchart.jpg", alt: "Keyword Network", description: "Keyword Network: Shows the correlation between keywords and topics", bgColor: "#99ceff" },
    { src: "/imgs/new-geographychart.jpg", alt: "Geographic Charts", description: "Geographic Chart: Visualizes where the topic data can be found around the world.", bgColor: "#035db4" }
  ];

  return (
    // Possible-data-visualizations section (with descriptions when you hover on one)
    <div className="w-full bg-white py-20">
      <p className="text-[#005eb4] text-5xl text-center">Possible Data Visualizations</p>
      <p className="text-xl text-center mt-4">Hover over each one to explore more!</p>

      <div className="flex flex-col items-center mt-16 space-y-32">
        <div className="flex justify-center gap-48">
          {visualizations.slice(0, 3).map((viz, index) => (
            <div
              key={index}
              className="relative group p-6 rounded-2xl"
              style={{ backgroundColor: viz.bgColor }}
            >
              <Image src={viz.src} alt={viz.alt} width={150} height={150} className="rounded-lg" />
              
              <div className="absolute inset-0 flex justify-center items-center bg-black bg-opacity-60 text-white text-sm px-6 py-4 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                {viz.description}
              </div>
            </div>
          ))}
        </div>

        <div className="flex justify-center gap-44">
          {visualizations.slice(3).map((viz, index) => (
            <div
              key={index}
              className="relative group p-6 rounded-2xl"
              style={{ backgroundColor: viz.bgColor }}
            >
              <Image src={viz.src} alt={viz.alt} width={150} height={150} className="rounded-lg" />
              
              <div className="absolute inset-0 flex justify-center items-center bg-black bg-opacity-60 text-white text-sm px-6 py-4 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                {viz.description}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

