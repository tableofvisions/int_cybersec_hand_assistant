"use server";
import "server-only";
import { CustomFormState } from "@/types";
import { registerSchema, reminderSchema, setPasswordSchema } from "../schemes/authentication.schemes";
import {
  REGISTER_FORM_GENERAL_ERROR_MESSAGE,
  REGISTER_FORM_SUCCESS_MESSAGE,
  REGISTER_FORM_USER_EXISTS_ERROR_MESSAGE,
  REQUEST_SUBMIT_SUCCESS_MESSAGE,
  RESET_PASSWORD_GENERAL_ERROR_MESSAGE,
  RESET_PASSWORD_SUCCESS_MESSAGE,
  RESET_PASSWORD_TOKEN_ERROR_MESSAGE,
  UNKNOWN_USER_NAME_MESSAGE,
  UNKOWN_SERVER_ERROR_MESSAGE,
} from "@/constants/dialog";
import { handleError } from "../utils";

export const verifyEmailRequest = async (token: string): Promise<boolean> => {
  try {
    if (!token) return false;
    const res = await fetch(`${process.env.BACKEND_API_URL}/auth/verify`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token }),
    });
    return res.ok;
  } catch (error) {
    handleError(error);
    return false;
  }
};

export const submitPasswordResetRequest = async (
  prevState: CustomFormState,
  data: FormData
): Promise<CustomFormState> => {
  try {
    const formData = Object.fromEntries(data);
    const fields: Record<string, string> = {};
    for (const key of Object.keys(formData)) {
      const v = formData[key]; if (typeof v === "string") fields[key] = v;
    }
    const parse = reminderSchema.safeParse(formData);
    if (!parse.success) {
      return { errors: parse.error.flatten().fieldErrors, message: UNKNOWN_USER_NAME_MESSAGE, success: false, fields };
    }
    const res = await fetch(`${process.env.BACKEND_API_URL}/auth/reset-request`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: parse.data.mail }),
    });
    if (res.ok) return { success: true, message: REQUEST_SUBMIT_SUCCESS_MESSAGE, fields };
    return { success: false, message: UNKOWN_SERVER_ERROR_MESSAGE };
  } catch (error) {
    handleError(error);
    return { success: false, message: UNKOWN_SERVER_ERROR_MESSAGE };
  }
};

export const resetPassword = async (
  prevState: CustomFormState,
  data: FormData
): Promise<CustomFormState> => {
  try {
    const formData = Object.fromEntries(data);
    const fields: Record<string, string> = {};
    for (const key of Object.keys(formData)) {
      const v = formData[key]; if (typeof v === "string") fields[key] = v;
    }
    const parse = setPasswordSchema.safeParse(formData);
    if (!parse.success) {
      return { errors: parse.error.flatten().fieldErrors, message: RESET_PASSWORD_GENERAL_ERROR_MESSAGE, success: false, fields };
    }
    const res = await fetch(`${process.env.BACKEND_API_URL}/auth/reset`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token: parse.data.token, new_password: parse.data.password }),
    });
    if (res.ok) return { success: true, message: RESET_PASSWORD_SUCCESS_MESSAGE, fields };
    if (res.status === 400) return { success: false, message: RESET_PASSWORD_TOKEN_ERROR_MESSAGE, fields, errors: { token: ["invalid token"] } };
    return { success: false, message: RESET_PASSWORD_GENERAL_ERROR_MESSAGE };
  } catch (error) {
    handleError(error);
    return { success: false, message: UNKOWN_SERVER_ERROR_MESSAGE };
  }
};

export const registerAccount = async (
  prevState: CustomFormState,
  data: FormData
): Promise<CustomFormState> => {
  try {
    const flat = Object.fromEntries(data);
    const fields: Record<string, string> = {};
    for (const key of Object.keys(flat)) {
      const v = flat[key]; if (typeof v === "string") fields[key] = v;
    }
    // FormData dot-notation keys stay flat; reconstruct nested objects for Zod
    const formData = {
      ...flat,
      mails: {
        mail: flat["mails.mail"],
        mailConfirm: flat["mails.mailConfirm"],
      },
      passwords: {
        password: flat["passwords.password"],
        passwordConfirm: flat["passwords.passwordConfirm"],
      },
    };
    const parse = registerSchema.safeParse(formData);
    if (!parse.success) {
      return {
        success: false,
        message: REGISTER_FORM_GENERAL_ERROR_MESSAGE,
        errors: parse.error.errors.reduce((acc: Record<string, string[]>, item) => {
          const path = item.path.join(".");
          if (!acc[path]) acc[path] = [];
          acc[path].push(item.message);
          return acc;
        }, {}),
        fields,
      };
    }

    const res = await fetch(`${process.env.BACKEND_API_URL}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: parse.data.mails?.mail ?? "",
        password: parse.data.passwords?.password ?? "",
        first_name: parse.data.firstName,
        last_name: parse.data.lastName,
        company_name: parse.data.name,
        location_id: parse.data.locationId ? Number(parse.data.locationId) : null,
        profession_id: parse.data.professionId ? Number(parse.data.professionId) : null,
        size_class: parse.data.companyType ?? null,
      }),
    });

    if (res.status === 201) return { success: true, message: REGISTER_FORM_SUCCESS_MESSAGE, fields };
    if (res.status === 409) return { success: false, errors: { "mails.mail": [REGISTER_FORM_USER_EXISTS_ERROR_MESSAGE] }, message: REGISTER_FORM_USER_EXISTS_ERROR_MESSAGE, fields };
    if (res.status === 422) {
      try {
        const body = await res.json() as { detail?: { loc?: string[]; msg?: string }[] | string };
        if (Array.isArray(body.detail)) {
          const errors: Record<string, string[]> = {};
          body.detail.forEach((d) => {
            const field = d.loc?.slice(1).join(".") ?? "general";
            const fieldKey = field === "password" ? "passwords.password" : field;
            if (!errors[fieldKey]) errors[fieldKey] = [];
            errors[fieldKey].push(d.msg ?? "Ungültige Eingabe");
          });
          return { success: false, errors, message: REGISTER_FORM_GENERAL_ERROR_MESSAGE, fields };
        }
      } catch (_) { /* fall through */ }
    }
    return { success: false, message: REGISTER_FORM_GENERAL_ERROR_MESSAGE, fields };
  } catch (error) {
    handleError(error);
    return { success: false, message: REGISTER_FORM_GENERAL_ERROR_MESSAGE };
  }
};

// kept for backward compat — same as registerAccount
export const submitRegisterForm = registerAccount;
