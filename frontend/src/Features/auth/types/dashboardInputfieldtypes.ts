import { FieldErrors, UseFormRegister } from "react-hook-form";
import { IPatientFormInput } from "@/types/patientStore";

interface InputFieldProps {
  id: keyof IPatientFormInput  ; // ensures `id` matches a valid form field
  label: string;
  register: UseFormRegister<IPatientFormInput>; // react-hook-form register function
  errors: FieldErrors<IPatientFormInput>; // errors object from react-hook-form
  required?: boolean;
  placeholder?: string;
  type?: string;
}
export type { InputFieldProps };