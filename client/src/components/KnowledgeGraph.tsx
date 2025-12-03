import { Link } from "wouter";
import { ArrowRight, GitCommit, Share2 } from "lucide-react";
import { Capsule } from "@/lib/data";

interface KnowledgeGraphProps {
  links: Capsule["links"];
}

export function KnowledgeGraph({ links }: KnowledgeGraphProps) {
  const hasLinks =
    links.parent.length > 0 ||
    links.children.length > 0 ||
    links.related.length > 0;

  if (!hasLinks) return null;

  return (
    <div className="border-t border-border pt-12 mt-12">
      <div className="flex items-center gap-2 mb-8">
        <Share2 className="w-5 h-5 text-primary" />
        <h2 className="text-2xl font-bold uppercase tracking-tight">
          Connected Experiences
        </h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Parent Nodes */}
        {links.parent.length > 0 && (
          <div className="space-y-4">
            <h3 className="text-xs font-bold uppercase text-muted-foreground flex items-center gap-2">
              <GitCommit className="w-4 h-4 rotate-90" /> Part of
            </h3>
            <div className="space-y-2">
              {links.parent.map(link => (
                <Link key={link} href={`/capsule/${link}`}>
                  <a className="block p-4 bg-secondary/30 border border-border hover:border-primary transition-all hover:-translate-y-1 group">
                    <div className="flex justify-between items-center">
                      <span className="font-bold text-sm uppercase truncate">
                        {link}
                      </span>
                      <ArrowRight className="w-4 h-4 text-muted-foreground group-hover:text-primary transition-colors" />
                    </div>
                  </a>
                </Link>
              ))}
            </div>
          </div>
        )}

        {/* Child Nodes */}
        {links.children.length > 0 && (
          <div className="space-y-4">
            <h3 className="text-xs font-bold uppercase text-muted-foreground flex items-center gap-2">
              <GitCommit className="w-4 h-4" /> Includes
            </h3>
            <div className="space-y-2">
              {links.children.map(link => (
                <Link key={link} href={`/capsule/${link}`}>
                  <a className="block p-4 bg-secondary/30 border border-border hover:border-primary transition-all hover:-translate-y-1 group">
                    <div className="flex justify-between items-center">
                      <span className="font-bold text-sm uppercase truncate">
                        {link}
                      </span>
                      <ArrowRight className="w-4 h-4 text-muted-foreground group-hover:text-primary transition-colors" />
                    </div>
                  </a>
                </Link>
              ))}
            </div>
          </div>
        )}

        {/* Related Nodes */}
        {links.related.length > 0 && (
          <div className="space-y-4">
            <h3 className="text-xs font-bold uppercase text-muted-foreground flex items-center gap-2">
              <GitCommit className="w-4 h-4" /> See Also
            </h3>
            <div className="space-y-2">
              {links.related.map(link => (
                <Link key={link} href={`/capsule/${link}`}>
                  <a className="block p-4 bg-secondary/30 border border-border hover:border-primary transition-all hover:-translate-y-1 group">
                    <div className="flex justify-between items-center">
                      <span className="font-bold text-sm uppercase truncate">
                        {link}
                      </span>
                      <ArrowRight className="w-4 h-4 text-muted-foreground group-hover:text-primary transition-colors" />
                    </div>
                  </a>
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
