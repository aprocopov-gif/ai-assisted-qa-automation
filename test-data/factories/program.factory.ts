import { faker } from '@faker-js/faker';

export type ProgramInput = {
  name: string;
  description: string;
};

/**
 * Happy-path program payload. Names are unique per call so parallel runs do not collide.
 */
export function buildProgram(
  overrides: Partial<ProgramInput> = {},
): ProgramInput {
  return {
    name: `AP_${faker.commerce.department()} ${Date.now()}`,
    description: faker.lorem.sentence(),
    ...overrides,
  };
}
