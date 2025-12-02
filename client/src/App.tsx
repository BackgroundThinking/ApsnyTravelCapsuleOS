import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFound from "@/pages/NotFound";
import { Route, Switch } from "wouter";
import ErrorBoundary from "./components/ErrorBoundary";
import { ThemeProvider } from "./contexts/ThemeContext";
import Home from "./pages/Home";
import CapsulePage from "./pages/CapsulePage";
import CategoryPage from "./pages/CategoryPage";


function Router() {
  return (
    <Switch>
      <Route path={"/"} component={Home} />
      
      {/* Category Routes */}
      <Route path="/tours">
        <CategoryPage 
          type="product" 
          title="Curated Tours" 
          description="Expertly crafted winter experiences in Abkhazia."
          heroImage="/images/hero-skitouring.jpg"
        />
      </Route>
      <Route path="/places">
        <CategoryPage 
          type="place" 
          title="Destinations" 
          description="Explore the hidden gems and iconic landmarks of the region."
          heroImage="/images/hero-gagra-colonnade.jpg"
        />
      </Route>
      <Route path="/guides">
        <CategoryPage 
          type="guide" 
          title="Travel Guides" 
          description="Essential tips and advice for your winter journey."
          heroImage="/images/hero-winter-ritsa.jpg"
        />
      </Route>

      <Route path={"/capsule/:slug*"} component={CapsulePage} />
      <Route path={"/404"} component={NotFound} />
      {/* Final fallback route */}
      <Route component={NotFound} />
    </Switch>
  );
}

// NOTE: About Theme
// - First choose a default theme according to your design style (dark or light bg), than change color palette in index.css
//   to keep consistent foreground/background color across components
// - If you want to make theme switchable, pass `switchable` ThemeProvider and use `useTheme` hook

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider
        defaultTheme="light"
        // switchable
      >
        <TooltipProvider>
          <Toaster />
          <Router />
        </TooltipProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
