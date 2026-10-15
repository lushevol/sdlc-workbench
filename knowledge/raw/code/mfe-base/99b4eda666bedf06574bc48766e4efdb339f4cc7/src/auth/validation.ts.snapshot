import { z } from "zod";

const openFinTokenSchema = z
  .string()
  .trim()
  .min(1)
  .max(8192)
  .refine((token) => !/[\u0000-\u001f\u007f]/.test(token));

const credentialsSchema = z
  .object({
    username: z.string().trim().min(1).max(256),
    password: z.string().min(1).max(4096),
  })
  .strict();

const authorizationCodeSchema = z
  .object({
    code: z.string().trim().min(1).max(4096),
    iss: z.string().url().optional(),
    client_id: z.string().trim().min(1).max(256).optional(),
  })
  .strict();

const loginRequestSchema = z.union([
  credentialsSchema,
  authorizationCodeSchema,
]);

export type LoginRequest = z.infer<typeof loginRequestSchema>;

export const validateOpenFinToken = (input: unknown) =>
  openFinTokenSchema.safeParse(input);

export const validateLoginRequest = (input: unknown) =>
  loginRequestSchema.safeParse(input);
