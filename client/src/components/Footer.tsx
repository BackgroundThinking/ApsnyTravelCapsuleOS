import { Link } from "wouter";

export function Footer() {
  return (
    <footer className="bg-sidebar text-sidebar-foreground border-t border-sidebar-border py-12 mt-auto">
      <div className="container grid grid-cols-1 md:grid-cols-4 gap-8">
        <div className="space-y-4">
          <Link href="/">
            <a className="text-xl font-bold tracking-tighter uppercase flex items-center gap-2">
              <span className="text-primary text-2xl">●</span>
              ApsnyTravel
            </a>
          </Link>
          <p className="text-sm text-muted-foreground max-w-xs">
            Your definitive guide to winter adventures in Abkhazia and Sochi.
            Curated tours, hidden gems, and expert advice.
          </p>
        </div>

        <div>
          <h4 className="font-bold uppercase mb-4 text-sm">Explore</h4>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li><Link href="/tours"><a className="hover:text-primary">Tours</a></Link></li>
            <li><Link href="/places"><a className="hover:text-primary">Places</a></Link></li>
            <li><Link href="/guides"><a className="hover:text-primary">Guides</a></Link></li>
          </ul>
        </div>

        <div>
          <h4 className="font-bold uppercase mb-4 text-sm">Company</h4>
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li><Link href="/about"><a className="hover:text-primary">About Us</a></Link></li>
            <li><Link href="/contact"><a className="hover:text-primary">Contact</a></Link></li>
            <li><Link href="/privacy"><a className="hover:text-primary">Privacy Policy</a></Link></li>
          </ul>
        </div>

        <div>
          <h4 className="font-bold uppercase mb-4 text-sm">Newsletter</h4>
          <p className="text-sm text-muted-foreground mb-4">
            Subscribe for the latest winter updates.
          </p>
          <div className="flex gap-2">
            <input
              type="email"
              placeholder="EMAIL"
              className="bg-background border border-input px-3 py-2 text-sm w-full focus:outline-none focus:ring-1 focus:ring-primary"
            />
            <button className="bg-primary text-primary-foreground px-4 py-2 text-sm font-bold uppercase hover:bg-primary/90">
              →
            </button>
          </div>
        </div>
      </div>
      <div className="container mt-12 pt-8 border-t border-sidebar-border flex flex-col md:flex-row justify-between items-center text-xs text-muted-foreground uppercase">
        <p>© 2025 ApsnyTravel. All rights reserved.</p>
        <p>Designed with Swiss Precision</p>
      </div>
    </footer>
  );
}
