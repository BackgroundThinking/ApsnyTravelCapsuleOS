import { useEffect, useState } from "react";
import { Link } from "wouter";
import { Navigation } from "@/components/Navigation";
import { Footer } from "@/components/Footer";
import { fetchCapsules, Capsule } from "@/lib/data";
import { ArrowRight, MapPin, Thermometer, Mountain, Compass } from "lucide-react";

export default function Home() {
  const [capsules, setCapsules] = useState<Capsule[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCapsules().then((data) => {
      setCapsules(data);
      setLoading(false);
    });
  }, []);

  const featuredTours = capsules.filter(c => c.tier === 1).slice(0, 3);
  const featuredPlaces = capsules.filter(c => c.tier === 2 && c.type === 'place').slice(0, 4);

  return (
    <div className="min-h-screen flex flex-col bg-background font-sans">
      <Navigation />

      {/* Hero Section */}
      <section className="relative h-screen w-full overflow-hidden">
        <div className="absolute inset-0">
          <img
            src="/images/hero-winter-ritsa.jpg"
            alt="Lake Ritsa Winter"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-black/20" />
        </div>
        
        <div className="relative container h-full flex flex-col justify-center z-10 text-white">
          <div className="max-w-4xl space-y-6">
            <div className="inline-flex items-center gap-2 border border-white/30 bg-white/10 backdrop-blur-sm px-4 py-1 text-sm font-medium uppercase tracking-wider">
              <span className="w-2 h-2 rounded-full bg-primary animate-pulse" />
              Winter Season 2025
            </div>
            <h1 className="text-6xl md:text-8xl font-bold tracking-tighter leading-none uppercase">
              Abkhazia <br />
              <span className="text-transparent stroke-text">Winter</span>
            </h1>
            <p className="text-xl md:text-2xl max-w-2xl font-light text-white/90">
              Discover the silent majesty of the Caucasus. From frozen alpine lakes to steaming thermal springs.
            </p>
            <div className="flex gap-4 pt-8">
              <Link href="/tours">
                <a className="bg-primary text-white px-8 py-4 text-lg font-bold uppercase tracking-wide hover:bg-primary/90 transition-colors">
                  Explore Tours
                </a>
              </Link>
              <Link href="/places">
                <a className="bg-white text-black px-8 py-4 text-lg font-bold uppercase tracking-wide hover:bg-white/90 transition-colors">
                  View Map
                </a>
              </Link>
            </div>
          </div>
        </div>

        {/* Scroll Indicator */}
        <div className="absolute bottom-12 left-1/2 -translate-x-1/2 animate-bounce text-white">
          <ArrowRight className="rotate-90 w-6 h-6" />
        </div>
      </section>

      {/* Introduction Grid */}
      <section className="py-24 bg-background">
        <div className="container">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-16 items-center">
            <div className="space-y-8">
              <h2 className="text-4xl md:text-5xl font-bold uppercase tracking-tight">
                The Winter <span className="text-primary">Contrast</span>
              </h2>
              <p className="text-lg text-muted-foreground leading-relaxed">
                Abkhazia in winter is a land of striking contrasts. In the morning, you can be freeriding on the virgin slopes of the Caucasus Mountains, and by evening, relaxing in hot thermal springs surrounded by eucalyptus groves.
              </p>
              <div className="grid grid-cols-2 gap-8 pt-4">
                <div className="space-y-2">
                  <Thermometer className="w-8 h-8 text-primary" />
                  <h3 className="font-bold uppercase">Thermal Springs</h3>
                  <p className="text-sm text-muted-foreground">Natural healing waters open year-round.</p>
                </div>
                <div className="space-y-2">
                  <Mountain className="w-8 h-8 text-primary" />
                  <h3 className="font-bold uppercase">Alpine Skiing</h3>
                  <p className="text-sm text-muted-foreground">Pristine slopes and backcountry routes.</p>
                </div>
              </div>
            </div>
            <div className="relative aspect-[4/5] bg-muted">
              <img 
                src="/images/hero-new-athos.jpg" 
                alt="New Athos" 
                className="w-full h-full object-cover grayscale hover:grayscale-0 transition-all duration-700"
              />
              <div className="absolute -bottom-8 -left-8 bg-white p-8 shadow-xl max-w-xs hidden md:block">
                <p className="font-mono text-xs text-muted-foreground mb-2">LOCATION</p>
                <p className="font-bold uppercase text-lg">New Athos Monastery</p>
                <p className="text-sm mt-2">Founded in 1875, a spiritual center amidst the mountains.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Tours */}
      <section className="py-24 bg-secondary/30">
        <div className="container">
          <div className="flex justify-between items-end mb-12">
            <div>
              <h2 className="text-4xl font-bold uppercase tracking-tight mb-2">Curated Tours</h2>
              <p className="text-muted-foreground">Handpicked experiences for the discerning traveler.</p>
            </div>
            <Link href="/tours">
              <a className="hidden md:flex items-center gap-2 font-bold uppercase text-sm hover:text-primary transition-colors">
                View All Tours <ArrowRight className="w-4 h-4" />
              </a>
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {loading ? (
              [1, 2, 3].map((i) => (
                <div key={i} className="aspect-[3/4] bg-muted animate-pulse" />
              ))
            ) : (
              featuredTours.map((tour) => (
                <Link key={tour.id} href={`/capsule/${tour.slug}`}>
                  <a className="group block relative aspect-[3/4] overflow-hidden bg-black">
                    <img
                      src={`/images/hero-${tour.slug.includes('ritsa') ? 'winter-ritsa' : tour.slug.includes('athos') ? 'new-athos' : 'skitouring'}.jpg`}
                      alt={tour.title}
                      className="w-full h-full object-cover opacity-80 group-hover:opacity-60 group-hover:scale-105 transition-all duration-500"
                    />
                    <div className="absolute inset-0 p-8 flex flex-col justify-between text-white">
                      <div className="flex justify-between items-start">
                        <span className="border border-white/30 px-2 py-1 text-xs font-bold uppercase backdrop-blur-sm">
                          {tour.duration}
                        </span>
                        <span className="text-2xl">{tour.emoji}</span>
                      </div>
                      <div>
                        <h3 className="text-2xl font-bold uppercase leading-tight mb-2 group-hover:translate-x-2 transition-transform">
                          {tour.title}
                        </h3>
                        <p className="text-sm text-white/80 line-clamp-2 opacity-0 group-hover:opacity-100 transition-opacity delay-100">
                          {tour.seo.description}
                        </p>
                      </div>
                    </div>
                  </a>
                </Link>
              ))
            )}
          </div>
        </div>
      </section>

      {/* Places Grid */}
      <section className="py-24 bg-background">
        <div className="container">
          <div className="mb-16 text-center max-w-2xl mx-auto">
            <h2 className="text-4xl font-bold uppercase tracking-tight mb-4">Destinations</h2>
            <p className="text-muted-foreground">
              Explore the diverse landscapes of the region. From the Black Sea coast to the high peaks of the Caucasus.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-px bg-border border border-border">
            {loading ? (
              [1, 2, 3, 4].map((i) => (
                <div key={i} className="aspect-square bg-background animate-pulse" />
              ))
            ) : (
              featuredPlaces.map((place) => (
                <Link key={place.id} href={`/capsule/${place.slug}`}>
                  <a className="bg-background p-8 aspect-square flex flex-col justify-between hover:bg-secondary/50 transition-colors group">
                    <div className="flex justify-between items-start">
                      <MapPin className="w-6 h-6 text-muted-foreground group-hover:text-primary transition-colors" />
                      <span className="text-xs font-mono text-muted-foreground">
                        {place.geo.lat.toFixed(2)}, {place.geo.lng.toFixed(2)}
                      </span>
                    </div>
                    <div>
                      <h3 className="text-xl font-bold uppercase mb-2">{place.title}</h3>
                      <p className="text-sm text-muted-foreground line-clamp-2">
                        {place.seo.description}
                      </p>
                    </div>
                  </a>
                </Link>
              ))
            )}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-32 bg-sidebar text-sidebar-foreground relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
           <img src="/images/hero-gagra-colonnade.jpg" className="w-full h-full object-cover grayscale" />
        </div>
        <div className="container relative z-10 text-center">
          <h2 className="text-5xl md:text-7xl font-bold uppercase tracking-tighter mb-8">
            Ready for <br /> Adventure?
          </h2>
          <p className="text-xl text-muted-foreground max-w-xl mx-auto mb-12">
            Book your winter tour now and experience the magic of Abkhazia with expert guides.
          </p>
          <button className="bg-primary text-white px-12 py-6 text-xl font-bold uppercase tracking-wide hover:bg-primary/90 transition-colors">
            Start Planning
          </button>
        </div>
      </section>

      <Footer />
    </div>
  );
}
