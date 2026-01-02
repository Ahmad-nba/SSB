// export type Status = "Checked In"|"Pre-Procedure"|"In Progress"|"Closing"|"Recovery"|"Complete"|"Dismissal"
export interface ICustodian {
  name: string;
  phoneNumber: string;
}

export interface IDoctor {
  id: number;
  fullName: string;
  specialization?: string;
}

// export interface IPatients {
//   patientNumber: string;
//   firstName: string;
//   lastName: string;
//   streetAddress: string;
//   city: string;
//   state: string;
//   country: string;
//   phoneNumber: string;
//   contactEmail: string;
//   status: Status;

//   // ✅ New Fields
//   custodian: ICustodian;      // Person responsible for the patient
//   assignedDoctor: IDoctor;    // Selected doctor from database
//   roomNumber: string;         // Patient’s assigned room
// }

// // ✅ Flattened version used in form only
// export interface IPatientFormInput {
//   patientNumber: string;
//   firstName: string;
//   lastName: string;
//   streetAddress: string;
//   city: string;
//   state: string;
//   country: string;
//   phoneNumber: string;
//   contactEmail: string;
//   status: Status;

//   // Flattened custodian fields
//   custodianName: string;
//   custodianPhone: string;
//   custodianEmail?: string;

//   // Doctor relation
//   doctor_id: number;

//   // Room assignment
//   roomNumber: string;
// }

export type Status =
  | "Checked In"
  | "Pre-Procedure"
  | "In Progress"
  | "Closing"
  | "Recovery"
  | "Complete"
  | "Dismissal";

export interface IPatientFormInput {
  patientNumber?: string;
  firstName: string;
  lastName: string;
  streetAddress: string;
  city: string;
  state: string;
  country: string;
  phoneNumber: string;
  contactEmail: string;
  status: Status;
  custodianName: string;
  custodianPhone: string;
  custodianEmail?: string;
  doctor_id: number;
  roomNumber: string;
  age: number; // new required field
  dateOfBirth: string; // new required field
  nationality?: string; // new required field
}

export interface IPatients extends IPatientFormInput {
  patientNumber: string; // always defined in saved patients
}
