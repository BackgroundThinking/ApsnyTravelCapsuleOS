import { useEffect, useRef } from "react";
import { MapView } from "@/components/Map";

interface CapsuleMapProps {
  lat: number;
  lng: number;
  title: string;
}

export function CapsuleMap({ lat, lng, title }: CapsuleMapProps) {
  const mapRef = useRef<google.maps.Map | null>(null);
  const markerRef = useRef<google.maps.Marker | null>(null);

  const handleMapReady = (map: google.maps.Map) => {
    mapRef.current = map;

    // Create marker
    markerRef.current = new google.maps.Marker({
      position: { lat, lng },
      map: map,
      title: title,
      animation: google.maps.Animation.DROP,
    });

    // Set view
    map.setCenter({ lat, lng });
    map.setZoom(14);

    // Style map (Grayscale / Swiss Style)
    map.setOptions({
      styles: [
        {
          featureType: "all",
          elementType: "labels.text.fill",
          stylers: [
            { saturation: 36 },
            { color: "#000000" },
            { lightness: 40 },
          ],
        },
        {
          featureType: "all",
          elementType: "labels.text.stroke",
          stylers: [
            { visibility: "on" },
            { color: "#000000" },
            { lightness: 16 },
          ],
        },
        {
          featureType: "all",
          elementType: "labels.icon",
          stylers: [{ visibility: "off" }],
        },
        {
          featureType: "administrative",
          elementType: "geometry.fill",
          stylers: [{ color: "#000000" }, { lightness: 20 }],
        },
        {
          featureType: "administrative",
          elementType: "geometry.stroke",
          stylers: [{ color: "#000000" }, { lightness: 17 }, { weight: 1.2 }],
        },
        {
          featureType: "landscape",
          elementType: "geometry",
          stylers: [{ color: "#000000" }, { lightness: 20 }],
        },
        {
          featureType: "poi",
          elementType: "geometry",
          stylers: [{ color: "#000000" }, { lightness: 21 }],
        },
        {
          featureType: "road.highway",
          elementType: "geometry.fill",
          stylers: [{ color: "#000000" }, { lightness: 17 }],
        },
        {
          featureType: "road.highway",
          elementType: "geometry.stroke",
          stylers: [{ color: "#000000" }, { lightness: 29 }, { weight: 0.2 }],
        },
        {
          featureType: "road.arterial",
          elementType: "geometry",
          stylers: [{ color: "#000000" }, { lightness: 18 }],
        },
        {
          featureType: "road.local",
          elementType: "geometry",
          stylers: [{ color: "#000000" }, { lightness: 16 }],
        },
        {
          featureType: "transit",
          elementType: "geometry",
          stylers: [{ color: "#000000" }, { lightness: 19 }],
        },
        {
          featureType: "water",
          elementType: "geometry",
          stylers: [{ color: "#0f172a" }, { lightness: 17 }],
        },
      ],
      disableDefaultUI: true,
      zoomControl: true,
    });
  };

  // Update marker when props change
  useEffect(() => {
    if (mapRef.current && markerRef.current) {
      const newPos = { lat, lng };
      markerRef.current.setPosition(newPos);
      mapRef.current.panTo(newPos);
      markerRef.current.setTitle(title);
    }
  }, [lat, lng, title]);

  return (
    <div className="w-full h-[300px] bg-muted border border-border mt-8 overflow-hidden grayscale hover:grayscale-0 transition-all duration-700">
      <MapView onMapReady={handleMapReady} />
    </div>
  );
}
