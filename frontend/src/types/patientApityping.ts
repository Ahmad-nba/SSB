import { Status } from "./patientStore";

interface PatientApiResponse {
  code: string;
  first_name: string;
  last_name: string;
  email: string;
  contact?: string;
  address?: string;
  district?: string;
  state?: string;
  country?: string;
  current_status?: Status;
  notes?: string;
}

export type { PatientApiResponse };
