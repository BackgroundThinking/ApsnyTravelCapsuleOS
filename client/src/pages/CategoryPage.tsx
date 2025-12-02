import { useEffect, useState } from "react";
import { Link, useRoute } from "wouter";
import { fetchCapsules, Capsule } from "@/lib/data";
import { Navigation } from "@/components/Navigation";
import { Footer } from "@/components/Footer";
import { ArrowRight, MapPin, Filter } from "lucide-react";

interface CategoryPageProps {
  type: "product" | "place" | "guide";
  title: string;
  description: string;
  heroImage: string;
}

export default function CategoryPage({ type, title, description, heroImage }: CategoryPageProps) {
  const [capsules, setCapsules] = useState<Capsule[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCapsules().then((data) => {
      // Filter capsules by type
      // Note: 'product' covers tours/transfers, 'place' covers places, 'guide' covers guides
      const filtered = data.filter(c => {
        if (type === 'product') return c.tier === 1; // Tier 1 are products/tours
        if (type === 'place') return c.tier === 2 && c.type === 'place';
        if (type === 'guide') return c.tier === 2 && c.type === 'guide';
        return false;
      });
      setCapsules(filtered);
      setLoading(false);
    });
  }, [type]);

  return (
    <div className="min-h-screen bg-background font-sans flex flex-col">
      <Navigation />

      {/* Hero Header */}
      <header className="relative h-[40vh] min-h-[300px] w-full overflow-hidden">
        <div className="absolute inset-0">
          <img
            src={heroImage}
            alt={title}
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-black/50" />
        </div>
        
        <div className="relative container h-full flex flex-col justify-center z-10 text-white">
          <div className="max-w-4xl space-y-4">
            <h1 className="text-5xl md:text-6xl font-bold tracking-tighter leading-none uppercase animate-in fade-in slide-in-from-bottom-4 duration-700">
              {title}
            </h1>
            <p className="text-xl max-w-2xl font-light text-white/90">
              {description}
            </p>
          </div>
        </div>
      </header>

      {/* Content Grid */}
      <main className="flex-1 container py-16">
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <div key={i} className="aspect-[4/3] bg-muted animate-pulse" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {capsules.map((capsule) => (
              <Link key={capsule.id} href={`/capsule/${capsule.slug}`}>
                <a className="group block bg-background border border-border hover:border-primary transition-all hover:-translate-y-1">
                  <div className="aspect-video overflow-hidden bg-muted relative">
                    {/* Placeholder image logic - in real app would use capsule specific images */}
                    <div className="absolute inset-0 flex items-center justify-center bg-secondary/30 text-4xl">
                      {capsule.emoji}
                    </div>
                  </div>
                  <div className="p-6 space-y-4">
                    <div className="flex justify-between items-start">
                      <span className="text-xs font-bold uppercase text-primary tracking-wider">
                        {capsule.seo.keywords[0]}
                      </span>
                      {capsule.geo && (
                        <span className="text-xs text-muted-foreground flex items-center gap-1">
                          <MapPin className="w-3 h-3" /> {capsule.geo.region}
                        </span>
                      )}
                    </div>
                    
                    <div>
                      <h3 className="text-xl font-bold uppercase leading-tight mb-2 group-hover:text-primary transition-colors">
                        {capsule.title}
                      </h3>
                      <p className="text-sm text-muted-foreground line-clamp-2">
                        {capsule.seo.description}
                      </p>
                    </div>

                    <div className="pt-4 border-t border-border flex justify-between items-center">
                      <span className="text-xs font-bold uppercase text-muted-foreground">View Details</span>
                      <ArrowRight className="w-4 h-4 text-muted-foreground group-hover:text-primary transition-colors" />
                    </div>
                  </div>
                </a>
              </Link>
            ))}
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
}
