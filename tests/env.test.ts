import { describe, expect, it } from "vitest";
import { envSchema } from "@/env";

describe("environment validation", () => {
  it("applies safe defaults when optional environment values are absent", () => {
    expect(envSchema.parse({})).toEqual({
      NODE_ENV: "development",
      APP_ENV: "development",
    });
  });

  it("rejects unsupported application environments", () => {
    expect(() => envSchema.parse({ APP_ENV: "invalid" })).toThrow();
  });
});
