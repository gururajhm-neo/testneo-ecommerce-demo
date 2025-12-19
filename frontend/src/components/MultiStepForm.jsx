import { useState } from 'react';
import { FiChevronLeft, FiChevronRight, FiCheck } from 'react-icons/fi';

/**
 * Multi-Step Form/Wizard Component for TestNeo Automation Testing
 * Features:
 * - Step navigation
 * - Form validation per step
 * - Progress indicator
 * - Step summary
 * - Conditional step rendering
 */
const MultiStepForm = ({
  steps = [],
  onSubmit,
  onStepChange,
  initialData = {},
  className = ''
}) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState(initialData);
  const [errors, setErrors] = useState({});
  const [completedSteps, setCompletedSteps] = useState(new Set());

  const updateFormData = (stepData) => {
    setFormData(prev => ({ ...prev, ...stepData }));
  };

  const validateStep = (stepIndex) => {
    const step = steps[stepIndex];
    if (!step.validate) return true;

    const stepErrors = step.validate(formData);
    setErrors(prev => ({ ...prev, [stepIndex]: stepErrors }));
    return !stepErrors || Object.keys(stepErrors).length === 0;
  };

  const handleNext = () => {
    if (validateStep(currentStep)) {
      setCompletedSteps(prev => new Set([...prev, currentStep]));
      if (currentStep < steps.length - 1) {
        const nextStep = currentStep + 1;
        setCurrentStep(nextStep);
        if (onStepChange) onStepChange(nextStep, formData);
      } else {
        handleSubmit();
      }
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
      if (onStepChange) onStepChange(currentStep - 1, formData);
    }
  };

  const handleStepClick = (stepIndex) => {
    // Only allow clicking on completed steps or next step
    if (stepIndex <= currentStep || completedSteps.has(stepIndex)) {
      setCurrentStep(stepIndex);
      if (onStepChange) onStepChange(stepIndex, formData);
    }
  };

  const handleSubmit = () => {
    if (validateStep(currentStep)) {
      if (onSubmit) {
        onSubmit(formData);
      }
    }
  };

  const currentStepComponent = steps[currentStep]?.component;

  return (
    <div className={`bg-white rounded-lg shadow-md ${className}`}>
      {/* Progress Indicator */}
      <div className="p-6 border-b">
        <div className="flex items-center justify-between">
          {steps.map((step, index) => (
            <div key={index} className="flex items-center flex-1">
              <div className="flex flex-col items-center flex-1">
                <button
                  onClick={() => handleStepClick(index)}
                  disabled={index > currentStep && !completedSteps.has(index)}
                  className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold transition-all ${
                    index < currentStep || completedSteps.has(index)
                      ? 'bg-green-500 text-white'
                      : index === currentStep
                      ? 'bg-primary-600 text-white ring-4 ring-primary-200'
                      : 'bg-gray-200 text-gray-600'
                  } ${index <= currentStep || completedSteps.has(index) ? 'cursor-pointer hover:scale-110' : 'cursor-not-allowed'}`}
                >
                  {completedSteps.has(index) ? <FiCheck /> : index + 1}
                </button>
                <div className={`mt-2 text-xs font-medium ${
                  index <= currentStep ? 'text-primary-600' : 'text-gray-400'
                }`}>
                  {step.title}
                </div>
              </div>
              {index < steps.length - 1 && (
                <div className={`flex-1 h-1 mx-2 ${
                  index < currentStep ? 'bg-green-500' : 'bg-gray-200'
                }`} />
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Step Content */}
      <div className="p-6">
        {currentStepComponent && (
          <div>
            {typeof currentStepComponent === 'function'
              ? currentStepComponent({
                  formData,
                  updateFormData,
                  errors: errors[currentStep] || {},
                  setErrors: (newErrors) => setErrors(prev => ({ ...prev, [currentStep]: newErrors }))
                })
              : currentStepComponent}
          </div>
        )}
      </div>

      {/* Navigation */}
      <div className="p-6 border-t flex justify-between">
        <button
          onClick={handlePrevious}
          disabled={currentStep === 0}
          className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
        >
          <FiChevronLeft /> Previous
        </button>
        <div className="text-sm text-gray-600 flex items-center">
          Step {currentStep + 1} of {steps.length}
        </div>
        <button
          onClick={handleNext}
          className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 flex items-center gap-2"
        >
          {currentStep === steps.length - 1 ? 'Submit' : 'Next'} <FiChevronRight />
        </button>
      </div>
    </div>
  );
};

export default MultiStepForm;

