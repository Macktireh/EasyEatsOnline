export type LoginPayload = {
  email: string;
  password: string;
}

export type SignupPayload = LoginPayload & {
  lastName: string;
  firstName: string;
  confirmPassword: string;
}
