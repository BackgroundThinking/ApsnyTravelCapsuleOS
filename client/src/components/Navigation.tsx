import { Link, useLocation } from "wouter";
import { cn } from "@/lib/utils";

export function Navigation() {
  const [location] = useLocation();

  const links = [
    { href: "/", label: "Explore" },
    { href: "/tours", label: "Tours" },
    { href: "/places", label: "Places" },
    { href: "/guides", label: "Guides" },
  ];

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/90 backdrop-blur-md border-b border-border h-16">
      <div className="container h-full flex items-center justify-between">
        <Link href="/">
          <a className="text-xl font-bold tracking-tighter uppercase flex items-center gap-2">
            <span className="text-primary text-2xl">●</span>
            ApsnyTravel
          </a>
        </Link>

        <div className="hidden md:flex items-center gap-8">
          {links.map(link => (
            <Link key={link.href} href={link.href}>
              <a
                className={cn(
                  "text-sm font-medium uppercase tracking-wide transition-colors hover:text-primary",
                  location === link.href
                    ? "text-primary border-b-2 border-primary"
                    : "text-muted-foreground"
                )}
              >
                {link.label}
              </a>
            </Link>
          ))}
        </div>

        <div className="flex items-center gap-4">
          <button className="text-sm font-bold uppercase bg-primary text-primary-foreground px-4 py-2 hover:bg-primary/90 transition-colors">
            Book Now
          </button>
        </div>
      </div>
    </nav>
  );
}
