type User = {
  id: string;
  email: string;
  password: string;
  role: string;
  name: {
    firstname: string;
    lastname: string;
  };
};

export const dummyUsers: User[] = [
  {
    id: "u1",
    email: "xyz@gmail.com",
    password: "admin123",
    role: "admin",
    name: { firstname: "Weston", lastname: "John" },
  },
  {
    id: "u2",
    email: "sarah@gmail.com",
    password: "cut123",
    role: "surgeon",
    name: { firstname: "Mitchele", lastname: "Sarah" },
  },
  {
    id: "u3",
    email: "path@gmail.com",
    password: "cut123",
    role: "surgeon",
    name: { firstname: "Lalji", lastname: "Path" },
  },
];
