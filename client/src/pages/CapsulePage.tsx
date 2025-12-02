import { useEffect, useState } from "react";
import { useRoute, Link } from "wouter";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { fetchCapsuleBySlug, Capsule } from "@/lib/data";
import { Navigation } from "@/components/Navigation";
import { Footer } from "@/components/Footer";
import { KnowledgeGraph } from "@/components/KnowledgeGraph";
import { CapsuleMap } from "@/components/CapsuleMap";
import { MapPin, Clock, Calendar, ArrowLeft, ArrowRight } from "lucide-react";
import { cn } from "@/lib/utils";

export default function CapsulePage() {
  const [match, params] = useRoute<any>("/capsule/:slug*");
  const [capsule, setCapsule] = useState<Capsule | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  // Wouter wildcard param is accessed via the param name defined in route
  const slug = params?.slug ? decodeURIComponent(params.slug) : "";

  useEffect(() => {
    if (!slug) return;

    setLoading(true);
    fetchCapsuleBySlug(slug)
      .then((data) => {
        if (data) {
          setCapsule(data);
          setError(false);
        } else {
          setError(true);
        }
        setLoading(false);
      })
      .catch(() => {
        setError(true);
        setLoading(false);
      });
  }, [slug]);

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex flex-col">
        <Navigation />
        <div className="flex-1 flex items-center justify-center">
          <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin" />
        </div>
      </div>
    );
  }

  if (error || !capsule) {
    return (
      <div className="min-h-screen bg-background flex flex-col">
        <Navigation />
        <div className="flex-1 flex flex-col items-center justify-center text-center p-4">
          <h1 className="text-4xl font-bold uppercase mb-4">Capsule Not Found</h1>
          <p className="text-muted-foreground mb-8">The requested data capsule could not be retrieved.</p>
          <Link href="/">
            <a className="bg-primary text-white px-6 py-3 font-bold uppercase hover:bg-primary/90 transition-colors">
              Return Home
            </a>
          </Link>
        </div>
      </div>
    );
  }

  // Determine hero image based on slug keywords (fallback logic)
  const getHeroImage = (slug: string) => {
    if (slug.includes('ritsa')) return '/images/hero-winter-ritsa.jpg';
    if (slug.includes('athos')) return '/images/hero-new-athos.jpg';
    if (slug.includes('gagra')) return '/images/hero-gagra-colonnade.jpg';
    if (slug.includes('thermal') || slug.includes('kyndyg')) return '/images/hero-thermal-springs.jpg';
    if (slug.includes('ski') || slug.includes('rosa')) return '/images/hero-skitouring.jpg';
    return '/images/hero-winter-ritsa.jpg'; // Default
  };

  return (
    <div className="min-h-screen bg-background font-sans flex flex-col">
      <Navigation />

      {/* Hero Header */}
      <header className="relative h-[60vh] min-h-[500px] w-full overflow-hidden group">
        <div className="absolute inset-0">
          <img
            src={getHeroImage(capsule.slug)}
            alt={capsule.title}
            className="w-full h-full object-cover transition-transform duration-[2s] ease-out group-hover:scale-105"
          />
          <div className="absolute inset-0 bg-black/40 transition-opacity duration-700 group-hover:bg-black/30" />
        </div>
        
        <div className="relative container h-full flex flex-col justify-end pb-16 z-10 text-white">
          <div className="max-w-4xl space-y-4">
            <div className="flex items-center gap-3 text-sm font-bold uppercase tracking-wider opacity-80">
              <span className="bg-primary px-2 py-1 text-white">{capsule.type}</span>
              <span>Tier {capsule.tier}</span>
              <span>•</span>
              <span>{capsule.seo.keywords[0]}</span>
            </div>
            
            <h1 className="text-5xl md:text-7xl font-bold tracking-tighter leading-none uppercase animate-in fade-in slide-in-from-bottom-4 duration-1000">
              {capsule.emoji} {capsule.title}
            </h1>
            
            <p className="text-xl md:text-2xl max-w-2xl font-light text-white/90 line-clamp-2">
              {capsule.seo.description}
            </p>
          </div>
        </div>
      </header>

      {/* Main Content Grid */}
      <main className="flex-1 container py-16">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
          
          {/* Sidebar: Metadata & Quick Facts */}
          <aside className="lg:col-span-4 space-y-8">
            <div className="bg-secondary/30 p-8 border border-border">
              <h3 className="font-bold uppercase mb-6 text-lg">Capsule Data</h3>
              
              <div className="space-y-4">
                <div className="flex items-start gap-3">
                  <MapPin className="w-5 h-5 text-primary shrink-0 mt-0.5" />
                  <div>
                    <p className="text-xs font-bold uppercase text-muted-foreground">Coordinates</p>
                    <p className="font-mono text-sm">{capsule.geo.lat.toFixed(4)}, {capsule.geo.lng.toFixed(4)}</p>
                  </div>
                </div>
                
                <CapsuleMap 
                  lat={capsule.geo.lat} 
                  lng={capsule.geo.lng} 
                  title={capsule.title} 
                />

                <div className="flex items-start gap-3">
                  <Clock className="w-5 h-5 text-primary shrink-0 mt-0.5" />
                  <div>
                    <p className="text-xs font-bold uppercase text-muted-foreground">Duration</p>
                    <p className="text-sm">{capsule.duration}</p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <Calendar className="w-5 h-5 text-primary shrink-0 mt-0.5" />
                  <div>
                    <p className="text-xs font-bold uppercase text-muted-foreground">Best Season</p>
                    <div className="flex flex-wrap gap-1 mt-1">
                      {capsule.season.map(s => (
                        <span key={s} className="text-xs border border-border px-1.5 py-0.5 capitalize bg-background">
                          {s}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Knowledge Graph Links */}
            {(capsule.links.parent.length > 0 || capsule.links.children.length > 0) && (
              <div className="space-y-4">
                <h3 className="font-bold uppercase text-sm text-muted-foreground">Connected Capsules</h3>
                
                {capsule.links.parent.map(link => (
                  <Link key={link} href={`/capsule/${link}`}>
                    <a className="block p-4 border border-border hover:border-primary transition-colors group">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs font-bold uppercase text-primary">Parent</span>
                        <ArrowRight className="w-4 h-4 -rotate-45 text-muted-foreground group-hover:text-primary transition-colors" />
                      </div>
                      <p className="font-bold truncate">{link}</p>
                    </a>
                  </Link>
                ))}

                {capsule.links.children.map(link => (
                  <Link key={link} href={`/capsule/${link}`}>
                    <a className="block p-4 border border-border hover:border-primary transition-colors group">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs font-bold uppercase text-muted-foreground">Child</span>
                        <ArrowRight className="w-4 h-4 text-muted-foreground group-hover:text-primary transition-colors" />
                      </div>
                      <p className="font-bold truncate">{link}</p>
                    </a>
                  </Link>
                ))}
              </div>
            )}
          </aside>

          {/* Main Content: Markdown Render */}
          <article className="lg:col-span-8">
            <div className="prose prose-lg max-w-none prose-headings:font-bold prose-headings:uppercase prose-headings:tracking-tight prose-a:text-primary prose-a:no-underline hover:prose-a:underline mb-16">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {capsule.content}
              </ReactMarkdown>
            </div>
            
            <KnowledgeGraph links={capsule.links} />
          </article>

        </div>
      </main>

      <Footer />
    </div>
  );
}
