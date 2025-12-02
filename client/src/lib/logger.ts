/**
 * Logger Utility
 * Provides structured logging for the application
 */

export enum LogLevel {
  DEBUG = 0,
  INFO = 1,
  WARN = 2,
  ERROR = 3,
}

export interface LogEntry {
  timestamp: string;
  level: string;
  message: string;
  data?: any;
  error?: Error;
}

class Logger {
  private level: LogLevel = LogLevel.INFO;
  private logs: LogEntry[] = [];
  private maxLogs: number = 1000;

  constructor(level: LogLevel = LogLevel.INFO) {
    this.level = level;
  }

  private formatTimestamp(): string {
    return new Date().toISOString();
  }

  private addLog(entry: LogEntry): void {
    this.logs.push(entry);
    if (this.logs.length > this.maxLogs) {
      this.logs.shift();
    }
  }

  private shouldLog(level: LogLevel): boolean {
    return level >= this.level;
  }

  debug(message: string, data?: any): void {
    if (this.shouldLog(LogLevel.DEBUG)) {
      const entry: LogEntry = {
        timestamp: this.formatTimestamp(),
        level: "DEBUG",
        message,
        data,
      };
      this.addLog(entry);
      console.debug(`[DEBUG] ${message}`, data);
    }
  }

  info(message: string, data?: any): void {
    if (this.shouldLog(LogLevel.INFO)) {
      const entry: LogEntry = {
        timestamp: this.formatTimestamp(),
        level: "INFO",
        message,
        data,
      };
      this.addLog(entry);
      console.info(`[INFO] ${message}`, data);
    }
  }

  warn(message: string, data?: any): void {
    if (this.shouldLog(LogLevel.WARN)) {
      const entry: LogEntry = {
        timestamp: this.formatTimestamp(),
        level: "WARN",
        message,
        data,
      };
      this.addLog(entry);
      console.warn(`[WARN] ${message}`, data);
    }
  }

  error(message: string, error?: Error | any, data?: any): void {
    if (this.shouldLog(LogLevel.ERROR)) {
      const entry: LogEntry = {
        timestamp: this.formatTimestamp(),
        level: "ERROR",
        message,
        error: error instanceof Error ? error : new Error(String(error)),
        data,
      };
      this.addLog(entry);
      console.error(`[ERROR] ${message}`, error, data);
    }
  }

  setLevel(level: LogLevel): void {
    this.level = level;
  }

  getLogs(): LogEntry[] {
    return [...this.logs];
  }

  clearLogs(): void {
    this.logs = [];
  }

  exportLogs(): string {
    return JSON.stringify(this.logs, null, 2);
  }
}

export const logger = new Logger(
  import.meta.env.DEV ? LogLevel.DEBUG : LogLevel.INFO
);
