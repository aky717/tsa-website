'use client'; 
import { useState, useEffect } from "react"; 
import { ChevronLeft, ChevronRight } from "lucide-react"; 
import { Card, CardContent } from "@/components/ui/card"; 
import Image from "next/image";

const items = [ 
  { id: 1, title: "Pie Charts", icon: "/imgs/new-piechart.jpg", background: "bg-[#007698]" }, 
  { id: 2, title: "Line Charts", icon: "/imgs/line-chart.jpg", background: "bg-[#042839]" }, 
  { id: 3, title: "Geographic Charts", icon: "/imgs/geographic-chart.jpg", background: "bg-[#007698]" }, 
  { id: 4, title: "Publication Count Charts", icon: "/imgs/publication-count-chart.jpg", background: "bg-[#005eb4]" }, 
  { id: 5, title: "Sunburst Charts", icon: "/imgs/sunburst-chart.jpg", background: "bg-[#042839]" }, 
  { id: 6, title: "Topics Over Time Charts", icon: "/imgs/topics-over-time-chart.jpg", background: "bg-[#007698]" }, 
  { id: 7, title: "Growth Bar Over Time Charts", icon: "/imgs/growth-bar-chart.jpg", background: "bg-[#005eb4]" },
];

export default function Carousel() { 
  const [activeIndex, setActiveIndex] = useState(0);
  const [autoSlide, setAutoSlide] = useState(true);

  const prevSlide = () => {
    setActiveIndex((prev) => (prev === 0 ? items.length - 3 : prev - 3));
    setAutoSlide(false);
  };

  const nextSlide = () => {
    setActiveIndex((prev) => (prev === items.length - 3 ? 0 : prev + 3));
    setAutoSlide(false);
  };

  const displayedItems = [
    items[(activeIndex + 0) % items.length],
    items[(activeIndex + 1) % items.length],
    items[(activeIndex + 2) % items.length],
  ];

  useEffect(() => {
    if (autoSlide) {
      const interval = setInterval(() => {
        setActiveIndex((prev) => (prev === items.length - 3 ? 0 : prev + 3));
      }, 4000);

      return () => clearInterval(interval);
    }
  }, [autoSlide]);

  return (
    <div className="relative flex items-center justify-center w-full max-w-6xl p-6 mx-auto">
      <button 
        onClick={prevSlide} 
        className="absolute left-0 p-4 bg-gray-100 border-2 border-[#d4ecff] rounded-full shadow-md top-1/2 transform -translate-y-1/2 hover:bg-gray-200 transition"
      >
        <ChevronLeft size={32} className="text-[#005eb4]" />
      </button>

      <div className="flex space-x-6 justify-center w-full overflow-hidden">
        {displayedItems.map((item, index) => (
          <Card
            key={item.id}
            className={`flex flex-col items-center justify-center p-10 w-80 h-80 transition-transform duration-500 ${item.background} text-white rounded-xl`} // Duration for smooth transition
          >
            <CardContent className="flex flex-col items-center">
              {item.icon.endsWith('.jpg') || item.icon.endsWith('.png') || item.icon.endsWith('.svg') ? (
                <Image
                  src={item.icon}
                  alt={item.title}
                  width={150}
                  height={150}
                  className="object-contain"
                />
              ) : (
                <span className="text-6xl">{item.icon}</span>
              )}
              <p className="mt-3 font-semibold text-center">{item.title}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <button 
        onClick={nextSlide} 
        className="absolute right-0 p-4 bg-gray-100 border-2 border-[#d4ecff] rounded-full shadow-md top-1/2 transform -translate-y-1/2 hover:bg-gray-200 transition"
      >
        <ChevronRight size={32} className="text-[#005eb4]" />
      </button>
    </div>
  );
}
