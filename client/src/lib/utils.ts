import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Combines multiple class names into a single string with Tailwind CSS conflict resolution
 * 
 * This utility function merges class names using clsx for conditional classes and
 * tailwind-merge to intelligently resolve Tailwind CSS class conflicts. When multiple
 * Tailwind classes target the same CSS property (e.g., "px-2" and "px-4"), tailwind-merge
 * ensures only the last one is applied, preventing style conflicts.
 * 
 * @param {...ClassValue[]} inputs - Any number of class values including strings, objects,
 *                                   arrays, or conditional expressions supported by clsx
 * @returns {string} A merged string of class names with conflicts resolved
 * 
 * @example
 * ```typescript
 * // Basic usage
 * cn("px-2 py-1", "bg-blue-500")
 * // Returns: "px-2 py-1 bg-blue-500"
 * 
 * // Conflict resolution
 * cn("px-2 py-1", "px-4")
 * // Returns: "py-1 px-4" (px-2 is overridden by px-4)
 * 
 * // Conditional classes
 * cn("base-class", { "active-class": isActive, "disabled-class": isDisabled })
 * 
 * // With component props
 * cn("default-styles", className)
 * ```
 * 
 * @remarks
 * This is a common pattern in React + Tailwind CSS applications for creating
 * flexible component APIs that accept additional class names via props while
 * maintaining proper Tailwind CSS specificity rules.
 * 
 * @see {@link https://github.com/dcastil/tailwind-merge|tailwind-merge}
 * @see {@link https://github.com/lukeed/clsx|clsx}
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
