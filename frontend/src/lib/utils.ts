import type { ClassValue } from "clsx";
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(...inputs));
}

export type Optional<T> = T | undefined | null;

export function hasValue<T>(value: Optional<T>): value is T {
  return value !== undefined && value !== null;
}

export function assertValue<T>(value: Optional<T>, message: string): T {
  if (value === undefined || value === null) throw new Error(message);
  return value;
}

export function isNumber(value: Optional<unknown>): value is number {
  return (
    typeof value === "number" && !Number.isNaN(value) && Number.isFinite(value)
  );
}

export function assertUnreachable(value: never): never {
  throw new Error(`Unreachable code reached with value: ${value}`);
}
