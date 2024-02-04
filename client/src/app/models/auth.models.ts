import { LoginPayload, SignupPayload } from "@/types/auth.types";

export class LoginModels {
  constructor(
    public email: string,
    public password: string
  ) { }

  /**
   * Create a LoginModels instance from the provided JSON payload.
   *
   * @param {LoginPayload} payload - the JSON payload containing email and password
   * @return {LoginModels} a new LoginModels instance
   */
  public static fromJson(payload: LoginPayload): LoginModels {
    return new LoginModels(
      payload.email,
      payload.password
    );
  }

  /**
   * Returns a LoginPayload object representing the current state of the LoginPayload.
   *
   * @return {LoginPayload} - the LoginPayload object
   */
  public toJson(): LoginPayload {
    return {
      email: this.email,
      password: this.password
    };
  }

}

export class SignupModels {
  constructor(
    public firstName: string,
    public lastName: string,
    public email: string,
    public password: string,
    public confirmPassword: string
  ) { }

  /**
   * Create a SignupModels instance from the given payload.
   *
   * @param {SignupPayload} payload - the payload for creating the SignupModels instance
   * @return {SignupModels} the created SignupModels instance
   */
  public static fromJson(payload: SignupPayload): SignupModels {
    return new SignupModels(
      payload.firstName,
      payload.lastName,
      payload.email,
      payload.password,
      payload.confirmPassword
    );
  }

  /**
   * Converts the object to a JSON representation.
   *
   * @return {SignupPayload} The JSON representation of the object.
   */
  public toJson(): SignupPayload {
    return {
      firstName: this.firstName,
      lastName: this.lastName,
      email: this.email,
      password: this.password,
      confirmPassword: this.confirmPassword
    };
  }
}
